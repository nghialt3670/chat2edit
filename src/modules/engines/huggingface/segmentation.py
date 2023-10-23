import numpy as np
from typing import Dict
from PIL import Image
from transformers import pipeline
import cv2


HF_CACHE_PATH = "D:/works/projects/test/src/modules/engines/huggingface/cache"
FACE_SEGMENTATION_MODEL_PATH = "jonathandinu/face-parsing" 
CLOTH_SEGMENTATION_MODEL_PATH = "mattmdjaga/segformer_b2_clothes"
GENERAL_SEGMENTATION_PATH = "facebook/detr-resnet-50-panoptic"

cloth_seg_pipe = pipeline("image-segmentation", model=CLOTH_SEGMENTATION_MODEL_PATH, cache_dir=HF_CACHE_PATH)
face_seg_pipe = pipeline("image-segmentation", model=FACE_SEGMENTATION_MODEL_PATH, cache_dir=HF_CACHE_PATH)
general_seg_pipe = pipeline("image-segmentation", model=GENERAL_SEGMENTATION_PATH, cache_dir=HF_CACHE_PATH)




def face_segment(image: np.ndarray) -> Dict[str, np.ndarray]:
    image = Image.fromarray(image)
    result = face_seg_pipe(image)
    masks = {obj["label"].lower(): np.array(obj["mask"]) for obj in result}
    return masks
    

def cloth_segment(image: np.ndarray) -> Dict[str, np.ndarray]:
    image = Image.fromarray(image)
    result = cloth_seg_pipe(image)
    masks = {obj["label"].lower(): np.array(obj["mask"]) for obj in result}
    return masks
    

def general_segment(image: np.ndarray) -> Dict[str, np.ndarray]:
    image = Image.fromarray(image)
    result = general_seg_pipe(image)
    masks = {obj["label"].lower(): np.array(obj["mask"]) for obj in result}
    return masks



