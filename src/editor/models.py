import numpy as np
from pydantic import BaseModel
from typing import List, Union, Set, Optional
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
    labels: Set[str]
    category: str
    uuid: str = uuid4()
    pos_x: int = 0
    pos_y: int = 0
    angle: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    flip_x: bool = False
    flip_y: bool = False
    filters: List[Filter] = []

    def __eq__(self, g: 'Graphic2D') -> bool:
        return g.__class__ == self.__class__ and g.uuid == self.uuid
    
    def __repr__(self) -> str:
        return str(self.__class__)


class BaseImage(Graphic2D):
    base64_str: str

    @property
    def image(self) -> Image.Image:
        if not hasattr(self, '_image'):
            self._image = base64_decode(self.base64_str)

        return self._image
    
    @property
    def base64_str(self) -> str:
        return self.__dict__['base64_str']
    
    @base64_str.setter
    def base64_str(self, base64_str: str) -> None:
        self.__dict__['base64_str'] = base64_str
        self._image = base64_decode(base64_str)
    
    @image.setter
    def image(self, image: Image.Image) -> None:
        self._image = image
        self.base64_str = base64_encode(image)
    
    def get_mask(self) -> np.ndarray:
        alpha_channel = self.image.split()[-1]
        mask = np.asarray(alpha_channel) 
        mask = np.where(mask == 0, 0, 255) 
        return mask
    
    def remove(
        self, mask: np.ndarray,
        inpainter: Optional[ImageInpainter] =  None
    ) -> None:
        if inpainter is not None:
            self.image = inpainter(self.image, mask)    

        inverted_mask = 255 - mask
        self.image.paste(
            Image.fromarray(inverted_mask), 
            (0, 0), Image.fromarray(mask)
        )

    def segment(self, labels: List[str], 
        segmenter: ZeroShotSegmenter
    ) -> List['ImageSegment']:
        entities = segmenter(self.image, labels)
        segments = []
        for e in entities:
            xmin, ymin, _, _ = Image.fromarray(e.mask).getbbox()
            segment = ImageSegment(
                category='image-segment',
                labels=e.labels,
                score=e.score,
                inpainted=False,
                base64_str='',
                pos_x=xmin,
                pos_y=ymin,
            )
            segment.image = cut_image_from_mask(self.image, e.mask)
            segments.append(segment)

        return segments


class ImageSegment(BaseImage):
    score: float
    inpainted: bool


class Text(Graphic2D):
    content: str
    font_family: str
    font_size: str
    font_style: str
    font_weight: Union[str, int]


