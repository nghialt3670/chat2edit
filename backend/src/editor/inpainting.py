import cv2
import torch
import numpy as np

from abc import ABC, abstractmethod
from PIL import Image
from typing import Tuple
from iopaint.model import LaMa
from iopaint.schema import InpaintRequest

from .utils import expand_mask


class ImageInpainter(ABC):
    @abstractmethod
    def __call__(
        self, 
        image: Image.Image,
        mask: np.ndarray,
    ) -> Image.Image:
        pass


class LaMaInpainter(LaMa, ImageInpainter):
    def __init__(
        self,
        model_path: str,
        device: str = 'cuda',
    ) -> None:
        self.model = torch.jit.load(model_path, 'cpu').eval().to(device)
        self.mask_expanding_iterations = 20
        self.device = device
        self.hd_strategy = "Resize"
        self.resize_limit = 1280

    def __call__(
        self, 
        image: Image.Image, 
        mask: np.ndarray, 
    ) -> Image.Image:
        image, mask = self._preprocess(image, mask)
        config = InpaintRequest(
            hd_strategy=self.hd_strategy, 
            hd_strategy_resize_limit=self.resize_limit
        )
        inpainted_image = super().__call__(image, mask, config)
        return Image.fromarray(inpainted_image.astype(np.uint8))
    
    def _preprocess(
        self, 
        image: Image.Image, 
        mask: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        mask = expand_mask(mask, self.mask_expanding_iterations)
        Image.fromarray(mask).save('expand_mask.png')
        return image, mask