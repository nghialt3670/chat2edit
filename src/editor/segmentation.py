import torch
import numpy as np
import groundingdino.datasets.transforms as T

from abc import ABC, abstractmethod
from dataclasses import dataclass
from segment_anything import SamPredictor, sam_model_registry
from groundingdino.util.inference import load_model, predict
from PIL import Image
from typing import Sequence, List, Tuple, Set
from torchvision.ops import box_convert

from .utils import post_process_mask, multi_label_nms


@dataclass
class SegmentEntity:
    labels: Set[str]
    box: Tuple[int, int, int, int]
    mask: np.ndarray
    score: float


class ZeroShotSegmenter(ABC):
    @abstractmethod
    def __call__(
        self, 
        image: Image.Image,
        target_labels: Sequence[str]
    ) -> List[SegmentEntity]: 
        pass


class GroundingDINOSAM(ZeroShotSegmenter):
    def __init__(
        self,
        gd_model_path: str,
        gd_config_path: str,
        sam_model_path: str,
        sam_model_type: str,
        gd_device: str = 'cuda',
        sam_device: str = 'cuda',
        box_threshold: float = 0.3,
        text_threshold: float = 0.25,
        nms_threshold: float = 0.6,
        box_expand_factor: float = 0.1,
    ) -> None:
        self.groundingdino = load_model(
            gd_config_path,
            gd_model_path,
            gd_device,
        )
        sam = sam_model_registry[sam_model_type](sam_model_path)
        sam.to(sam_device)
        self.sam = SamPredictor(sam)
        self.box_threshold = box_threshold
        self.text_threshold = text_threshold
        self.nms_threshold = nms_threshold
        self.box_expand_factor = box_expand_factor
        self.image = None

    def _set_image(
        self,
        image: Image.Image,
    ) -> None:
        self.image = image
        np_image = np.array(image.convert('RGB'))
        self.sam.set_image(np_image)

    def __call__(
        self,
        image: Image.Image,
        target_labels: Sequence[str],
    ) -> List[SegmentEntity]:
        self._set_image(image)

        label_sets = []
        box_scores = []
        boxes = []

        for target_label in target_labels:
            result = self._grounding_dino_detect(self.image, target_label)
            
            label_sets.extend([
                set([target_label, box_label]) 
                for box_label in result[0]
            ])
            box_scores.extend(result[1])
            boxes.extend(result[2])

        _, masks = self._sam_segment(
            self._expand_boxes(
                boxes, self.image.size[0], self.image.size[1],
            )
        )
        return [
            SegmentEntity(labels, box, mask, box_score) 
            for labels, box, mask, box_score in 
            zip(label_sets, boxes, masks, box_scores)
        ]
        
    def _grounding_dino_detect(
        self,
        image: Image.Image,
        label: str,
    ) -> Tuple[List[str], List[float], List[Tuple[int, int, int, int]]]:
        transformed_image = self._transform_image(image)
        caption = label + ' .'
        h, w, _ = np.asarray(image).shape
        boxes, logits, phrases = predict(
            model=self.groundingdino,
            image=transformed_image,
            caption=caption,
            box_threshold=self.box_threshold,
            text_threshold=self.text_threshold
        )
        boxes = box_convert(
            boxes=boxes * torch.Tensor([w, h, w, h]), 
            in_fmt="cxcywh", 
            out_fmt="xyxy"
        )
        labels = phrases
        scores = list(map(float, logits))
        boxes = list(map(tuple, boxes.numpy().astype(int)))
        return self._detection_filter(
            labels, scores, boxes 
        )
    
    def _sam_segment(
        self,
        boxes: Tuple[int, int, int, int],
    ) -> Tuple[List[float], List[np.ndarray]]:
        scores, masks = [], []
        for box in boxes:
            result = self.sam.predict(
                box=np.array(box),
                multimask_output=False,
            )
            masks.append(post_process_mask(
                np.array(result[0][0]).astype(np.uint8) * 255
            ))
            scores.append(float(result[1][0]))
        
        return scores, masks
        
    def _transform_image(
        self,
        image: Image.Image
    ) -> torch.Tensor:
        transform = T.Compose([
            T.RandomResize([800], max_size=1333),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])
        return transform(image.convert('RGB'), None)[0]
    
    def _detection_filter(
        self,
        labels: Sequence[str],
        scores: Sequence[float], 
        boxes: Sequence[Tuple[int, int, int, int]], 
    ) -> Tuple[List[str], List[float], List[Tuple[int, int, int, int]]]:
        filtered_labels, filtered_scores, filtered_boxes = [], [], []
        selected_indices = multi_label_nms(
            labels, scores, boxes, self.box_threshold, self.nms_threshold
        )
        for i in selected_indices:
            filtered_labels.append(labels[i])
            filtered_scores.append(scores[i])
            filtered_boxes.append(boxes[i])
        
        return filtered_labels, filtered_scores, filtered_boxes
        
    def _expand_boxes(
        self,
        boxes: Sequence[Tuple[int, int, int, int]],
        img_width: int,
        img_height: int,
    ) -> Sequence[Tuple[int, int, int]]:
        expanded_boxes = []
        for box in boxes:
            xmin, ymin, xmax, ymax = box
            x_offset = (xmax - xmin) * self.box_expand_factor / 2
            y_offset = (ymax - ymin) * self.box_expand_factor / 2
            xmin = max(0, xmin - x_offset)
            ymin = max(0, ymin - y_offset)
            xmax = min(img_width, xmax + y_offset)
            ymax = min(img_height, ymax + y_offset)
            expanded_boxes.append((xmin, ymin, xmax, ymax))

        return expanded_boxes