import cv2
import imagehash
import random
import numpy as np
import base64

from io import BytesIO
from PIL import Image
from typing import Sequence, List, Tuple, Dict
from scipy.ndimage import shift
from imutils import rotate
from cv2 import (
    BORDER_DEFAULT,
    MORPH_ELLIPSE,
    MORPH_OPEN,
    GaussianBlur,
    getStructuringElement,
    morphologyEx,
)


KERNEL = getStructuringElement(MORPH_ELLIPSE, (3, 3))


def group_indices_by_string(strings: List[str]) -> List[List[int]]:
    index_dict = {}
    for i, s in enumerate(strings):
        if s in index_dict:
            index_dict[s].append(i)
        else:
            index_dict[s] = [i]
    return list(index_dict.values())


def multi_label_nms(
    labels: Sequence[str],
    scores: Sequence[float], 
    boxes: Sequence[Tuple[int, int, int, int]], 
    score_threshold: float,
    nms_threshold: float,
) -> List[int]:
    grouped_indices = group_indices_by_string(labels)
    selected_indices = []
    for indices in grouped_indices:
        grouped_scores = np.array([scores[i] for i in indices])
        grouped_boxes = np.array([boxes[i] for i in indices])
        grouped_selected_indices = nms(
            grouped_scores, 
            grouped_boxes,
            score_threshold, 
            nms_threshold,
        )
        selected_indices.extend(grouped_selected_indices)
    return selected_indices


def nms(
    scores: Sequence[float], 
    boxes: Sequence[Tuple[int, int, int, int]], 
    score_threshold: float,
    nms_threshold: float,
) -> List[int]:
    return cv2.dnn.NMSBoxes(
        boxes, 
        scores, 
        score_threshold, 
        nms_threshold,
    )


def compare_images(image1, image2, hash_size=8) -> bool:
    hash1 = imagehash.phash(image1, hash_size=hash_size)
    hash2 = imagehash.phash(image2, hash_size=hash_size)
    return hash1 == hash2


def random_color_rgb():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


def iou(
    box1: Tuple[int, int, int, int], box2: Tuple[int, int, int, int]
) -> float:
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    # Calculate intersection area
    intersection_area = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
    
    # Calculate area of each box
    area_box1 = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    area_box2 = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)
    
    # Calculate union area
    union_area = area_box1 + area_box2 - intersection_area
    
    # Calculate IoU
    iou = intersection_area / union_area if union_area > 0 else 0
    
    return iou
    

def post_process_mask(mask: np.ndarray) -> np.ndarray:
    """
    Post Process the mask for a smooth boundary by applying Morphological Operations
    Research based on paper: https://www.sciencedirect.com/science/article/pii/S2352914821000757
    args:
        mask: Binary Numpy Mask
    """
    mask = morphologyEx(mask, MORPH_OPEN, KERNEL)
    mask = GaussianBlur(mask, (5, 5), sigmaX=2, sigmaY=2, borderType=BORDER_DEFAULT)
    mask = np.where(mask < 127, 0, 255).astype(np.uint8)  # type: ignore
    return mask


def expand_mask(mask: np.ndarray, iterations: int) -> np.ndarray:
    kernel = np.ones((3,3), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel, iterations=iterations)
    return dilated_mask


def base64_encode(image: Image.Image) -> str:
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes = image_bytes.getvalue()
    return base64.b64encode(image_bytes).decode("utf-8")


def base64_decode(data: str) -> Image.Image:
    image_bytes = base64.b64decode(data)
    image_stream = BytesIO(image_bytes)
    return Image.open(image_stream)


def cut_image_from_mask(image: Image.Image, mask: np.ndarray) -> Image.Image:
    box = Image.fromarray(mask).getbbox()
    xmin, ymin, xmax, ymax = box
    cut_image = Image.new('RGBA', (xmax - xmin, ymax - ymin))
    cut_image.paste(image.crop(box), (0, 0), Image.fromarray(mask))
    return cut_image
