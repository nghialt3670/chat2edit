import copy
import numpy as np
from dataclasses import dataclass
from typing import List, Union, Set, Optional, Any, Dict, Tuple, Literal
from uuid import uuid4
from PIL import Image

from .segmentation import ZeroShotSegmenter
from .utils import (
    base64_decode, 
    base64_encode, 
    cut_image_from_mask
)


class Filter:
    name: str
    value: float


@dataclass
class Transform:
    pos_x: int = 0
    pos_y: int = 0
    scale_x: float = 1.0
    scale_y: float = 1.0
    flip_x: bool = False
    flip_y: bool = False
    rotation: float = 0.0


class Graphic:
    def __init__(
        self,
        uid: Optional[str] = None,
        labels: Optional[Set[str]] = None,
        transform: Optional[Transform] = None,
    ) -> None:
        self.uid = uid or str(uuid4())
        self.labels = labels or set()
        self.transform = transform or Transform()

    @property
    def position(self) -> Tuple[int, int]:
        return (self.transform.pos_x, self.transform.pos_y)
    
    @position.setter
    def position(self, position: Tuple[int, int]) -> None:
        self.transform.pos_x = position[0]
        self.transform.pos_y = position[1]

    def label(self, labels: List[str]) -> 'Graphic':
        self.labels.update(labels)
        return self

    def shift(self, offsets: Tuple[int, int]) -> 'Graphic':
        self.transform.pos_x += offsets[0]
        self.transform.pos_y += offsets[1]
        return self

    def rotate(self, angle: float) -> 'Graphic':
        self.transform.rotation += angle
        return self
    
    def scale(self, factor: float) -> 'Graphic':
        return self.scale_horizontally(factor).scale_vertically(factor)
    
    def scale_horizontally(self, factor: float) -> 'Graphic':
        self.transform.scale_x *= factor
        return self
    
    def scale_vertically(self, factor: float) -> 'Graphic':
        self.transform.scale_y *= factor
        return self
    
    def flip(self, axis: Literal['x', 'y']) -> 'Graphic':
        return self.flip_horizontally() if axis == 'x' else self.flip_vertically()

    def flip_horizontally(self) -> 'Graphic':
        self.transform.flip_x = not self.transform.flip_x
        return self

    def flip_vertically(self) -> 'Graphic':
        self.transform.flip_y = not self.transform.flip_y
        return self
    
    def __eq__(self, graphic: 'Graphic') -> bool:
        return isinstance(graphic, self.__class__) and self.uid == graphic.uid
    
    def __hash__(self) -> int:
        return hash(self.uid)


class BaseImage(Graphic):
    def __init__(
        self, 
        data: Union[Image.Image, str],
        filters: Optional[List[Filter]] = None,
        uid: Optional[str] = None,
        labels: Optional[str] = None,
        transform: Optional[Transform] = None,
    ) -> None:
        super().__init__(uid, labels, transform)
        if isinstance(data, Image.Image):
            self._image = data
            self._base64 = base64_encode(data)
        elif isinstance (data, str):
            self._image = base64_decode(data)
            self._base64 = data
        else:
            raise ValueError('Invalid data input')
        
        self.filters = filters or []

    @property  
    def mask(self) -> np.ndarray:
        alpha_channel = self.image.split()[-1]
        mask = np.asarray(alpha_channel) 
        mask = np.where(mask == 0, 0, 255) 
        return mask
    
    @property
    def image(self) -> Image.Image:
        return self._image

    @image.setter
    def image(self, image: Image.Image) -> None:
        self._image = image
        self._base64 = base64_encode(image)

    @property
    def base64(self) -> str:
        return self._base64
    
    def copy(self) -> 'BaseImage':
        image_graphic = copy.deepcopy(self)
        image_graphic.image = self.image.copy()
        return image_graphic
    

class ImageSegment(BaseImage):
    def __init__(
        self, 
        data: Union[Image.Image, str],
        score: float,
        inpainted: Optional[bool] = None,
        filters: Optional[List[Filter]] = None,
        uid: Optional[str] = None,
        labels: Optional[str] = None,
        transform: Optional[Transform] = None,
    ) -> None:
        super().__init__(data, filters, uid, labels, transform)
        self.score = score
        self.inpainted = inpainted or False


class Text(Graphic):
    def __init__(
        self, 
        content: str,
        font_family: Optional[str] = None,
        font_style: Optional[str] = None,
        font_size: Optional[Union[str, int]] = None,
        font_weight: Optional[Union[str, int]] = None,
        uid: Optional[str] = None,
        labels: Optional[str] = None,
        transform: Optional[Transform] = None,
    ) -> None:
        super().__init__(uid, labels, transform)
        self.content = content
        self.font_family = font_family or 'auto'
        self.font_style = font_style or 'auto'
        self.font_size = font_size or 'auto'
        self.font_weight = font_weight or 'auto'



