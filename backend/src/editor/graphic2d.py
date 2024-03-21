import copy
import numpy as np
from pydantic import BaseModel
from typing import List, Union, Set, Optional, Any, Dict, Tuple, Literal
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

    @property
    def position(self) -> Tuple[int, int]:
        return (self.pos_x, self.pos_y)
    
    @position.setter
    def position(self, dest: Tuple[int, int]) -> 'Graphic2D':
        self.pos_x = dest[0]
        self.pos_y = dest[1]
        return self

    def shift(self, offsets: Tuple[int, int]) -> 'Graphic2D':
        self.pos_x += offsets[0]
        self.pos_y += offsets[1]
        return self

    def rotate(self, angle: float) -> 'Graphic2D':
        self.angle += angle

    def flip_horizontal(self) -> 'Graphic2D':
        self.flip_x = not self.flip_x
        return self

    def flip_vertical(self) -> 'Graphic2D':
        self.flip_y = not self.flip_y
        return self
    
    def flip(self, axis: Literal['x', 'y']) -> 'Graphic2D':
        if axis == 'x':
            return self.flip_horizontal()
        if axis == 'y':
            return self.flip_vertical()
            
    def scale_horizontal(self, factor: float) -> 'Graphic2D':
        self.scale_x *= factor
        return self
    
    def scale_vertical(self, factor: float) -> 'Graphic2D':
        self.scale_y *= factor

    def scale(self, factors: Tuple[float, float]) -> 'Graphic2D':
        return self.scale_horizontal(factors[0]).scale_vertical(factors[1])

    def apply(self, f: Filter) -> 'Graphic2D':
        self.filters.append(f)

    def label(self, label: str) -> 'Graphic2D':
        self.labels.add(label)

    def __eq__(self, g: 'Graphic2D') -> bool:
        return g.__class__ == self.__class__ and g.uuid == self.uuid
    
    def __repr__(self) -> str:
        return str(self.__class__)
    
    def __hash__(self) -> int:
        return hash(self.uuid)


class BaseImage(Graphic2D):
    base64_str: str

    @property
    def image(self) -> Image.Image:
        if not hasattr(self, '_image'):
            self._image = base64_decode(self.base64_str)

        return self._image
    
    @image.setter
    def image(self, image: Image.Image) -> None:
        self._image = image
        self.base64_str = base64_encode(image)
    
    @property
    def base64_str(self) -> str:
        return self.__dict__['base64_str']
    
    @base64_str.setter
    def base64_str(self, base64_str: str) -> None:
        self.__dict__['base64_str'] = base64_str
        self._image = base64_decode(base64_str)
    
    def get_mask(self) -> np.ndarray:
        alpha_channel = self.image.split()[-1]
        mask = np.asarray(alpha_channel) 
        mask = np.where(mask == 0, 0, 255) 
        return mask

    def segment(
        self, labels: List[str], 
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
            )
            segment.position = (xmin, ymin)
            segment.image = cut_image_from_mask(self.image, e.mask)
            segments.append(segment)

        return segments
    
    def __deepcopy__(
        self, memo: Optional[Dict[int, Any]] = None
    ) -> 'BaseImage':
        segment = copy.deepcopy(self)
        segment.image = self.image.copy()
        return segment


class ImageSegment(BaseImage):
    score: float    
    inpainted: bool


class Text(Graphic2D):
    content: str
    font_family: str
    font_size: str
    font_style: str
    font_weight: Union[str, int]



