import numpy as np
from typing import Dict
from PIL import Image
from transformers import pipeline


HF_CACHE_PATH = "./cache"
DETECTION_MODEL_PATH = "facebook/detr-resnet-101-dc5" 

det_pipe = pipeline("object-detection", model=DETECTION_MODEL_PATH, cache_dir=HF_CACHE_PATH)


def general_detect(image: np.ndarray) -> Dict[str, np.ndarray]:
    image = Image.fromarray(image)
    result = det_pipe(image)
    bboxes = {obj["label"].lower(): np.array(list(obj["box"].values())) for obj in result}
    return bboxes
    
    





