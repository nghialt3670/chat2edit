import numpy as np
from pydantic import BaseModel
from typing import List, Union, Set
from uuid import uuid4
from PIL import Image

from .segmentation import ZeroShotSegmenter
from .inpainting import ImageInpainter
from .utils import (
    base64_decode, 
    base64_encode, 
    cut_image_from_mask
)

class Filter(BaseModel):
    name: str
    value: float


class Graphic2D(BaseModel):
    category: str
    uuid: str = uuid4()
    pos_x: int = 0
    pos_y: int = 0
    angle: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    filters: List[Filter] = []

    def __eq__(self, g: 'Graphic2D') -> bool:
        return isinstance(g, Graphic2D) and g.uuid == self.uuid


class BaseImage(Graphic2D):
    base64_str: str

    @property
    def image(self) -> Image.Image:
        if not hasattr(self, 'image'):
            self.image = base64_decode(self.base64_str)

        return self.image
    
    @image.setter
    def image(self, image: Image.Image) -> None:
        self.image = image
        if self.base64_str == '':
            self.base64_str = base64_encode(image)

    @classmethod
    def from_pil(cls, image: Image.Image) -> 'BaseImage':
        instance = cls('')
        instance.image = image
        return instance
    
    def get_mask(self) -> np.ndarray:
        alpha_channel = self.image.split()[-1]
        mask = np.asarray(alpha_channel) 
        mask = np.where(mask == 0, 0, 255) 
        return mask


class ImageSegment(BaseImage):
    labels: Set[str]
    score: float

    @classmethod
    def from_segmenter(cls, image: Image.Image,
        labels: List[str], segmenter: ZeroShotSegmenter
    ) -> List['ImageSegment']:
        entities = segmenter(image, labels)
        segments = []
        for e in entities:
            xmin, ymin, _, _ = Image.fromarray(e.mask).getbbox()
            cut_image = cut_image_from_mask(image, e.mask)
            segment = cls.from_pil(cut_image)
            segment.pos_x = xmin
            segment.pos_y = ymin
            segments.append(segment)


class ImageInpaint(BaseImage):
    base64_str: str

    @classmethod
    def from_inpainter(cls, image: Image.Image, 
        mask: np.ndarray, inpainter: ImageInpainter
    ) -> 'ImageInpaint':
        inpainted_image = inpainter(image, mask)
        box = Image.fromarray(mask).getbbox()
        xmin, ymin, _, _ = box
        cut_image = cut_image_from_mask(inpainted_image, mask)
        inpaint = cls.from_pil(cut_image)
        inpaint.pos_x = xmin
        inpaint.pos_y = ymin
        return inpaint


class Text(Graphic2D):
    content: str
    font_family: str
    font_size: str
    font_style: str
    font_weight: Union[str, int]


class TargetImage(BaseImage):
    base64_str: str
    members: List[Union[ImageSegment, ImageInpaint, Text]]

