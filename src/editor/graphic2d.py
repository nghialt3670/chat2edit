import numpy as np

from typing import List, Tuple, Optional, Dict, Set, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from PIL import Image
from uuid import uuid4

from .segmentation import ZeroShotSegmenter 
from .inpainting import ImageInpainter
from .filter import Filter
from .utils import base64_encode, base64_decode


def apply_to_members(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        for g in self._graphics:
            func(g, *args, **kwargs)
    return wrapper


class Graphic2D(ABC):
    def __init__(self) -> None:
        self._uuid: str = str(uuid4()) 
        self._position: Tuple[int, int] = (0, 0)
        self._rotation: float = 0.0
        self._scale: Tuple[float, float] = (1.0, 1.0)
        self._flip_x: bool = False
        self._flip_y: bool = False
        self._filters: List[Filter] = []
        self._members: List[Graphic2D] = []
    
    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def position(self) -> Tuple[int, int]:
        return self._position
    
    @property
    def rotation(self) -> float:
        return self._rotation
    
    @property
    def scale_x(self) -> float:
        return self._scale[0]
    
    @property
    def scale_y(self) -> float:
        return self._scale[1]
    
    @property
    def flip_x(self) -> bool:
        return self._flip_x
    
    @property
    def flip_y(self) -> bool:
        return self._flip_y
    
    @property
    def filters(self) -> List[Filter]:
        return self._filters.copy()
    
    @property
    def members(self) -> List['Graphic2D']:
        return self._members.copy()
        
    @apply_to_members
    def move(self, offsets: Tuple[int, int]) -> None:
        self._position = (
            self._position[0] + offsets[0], 
            self._position[1] + offsets[1]
        )

    @apply_to_members
    def rotate(self, angle: float) -> None:
        self._angle += angle

    @apply_to_members
    def scale(self, factors: Tuple[float, float]) -> None:
        self._scale = (
            self._scale[0] * factors[0],
            self._scale[1] * factors[1]
        )

    @apply_to_members
    def flip_vertically(self) -> None:
        self._flip_x = not self._flip_x

    @apply_to_members
    def flip_horizontally(self) -> None:
        self._flip_y = not self._flip_y

    def add(self, g: 'Graphic2D') -> None:
        self._members.append(g) 

    def remove(self, g: 'Graphic2D') -> None:
        self._members.remove(g)

    def add_filter(self, f: Filter) -> None:
        self._filters.append(f)

    def set_properties(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __eq__(self, g: 'Graphic2D') -> bool:
        return self._uuid == g._uuid
    
    def __hash__(self) -> int:
        return hash(self.uuid)
    

class BasicImage(Graphic2D):
    def __init__(self, value: Image.Image) -> None:
        super().__init__()
        self._value = value

    @property
    def value(self) -> Image.Image:
        return self._value

    @classmethod
    def from_base64(cls, data: str) -> 'BasicImage':
        return cls(base64_decode(data))
    
    def base64_value(self) -> str:
        return base64_encode(self._value)


class ImageInpaint(BasicImage):
    def __init__(self, value: Image.Image) -> None:
        super().__init__(value)

    @classmethod
    def from_inpainter(cls, image: Image.Image, 
        mask: np.ndarray,inpainter: ImageInpainter) -> 'ImageInpaint':
        inpainted_image = inpainter(image, mask)
        mask_box = Image.fromarray(mask).getbbox()
        inpaint = cls(inpainted_image.crop(mask_box))
        inpaint.move((mask_box[0], mask_box[1]))
        return inpaint


class ImageSegment(BasicImage):
    def __init__(
        self, 
        labels: Set[str],
        score: float,
        value: Image.Image,
    ) -> None:
        super().__init__(value)
        self.labels = labels
        self.score = score
        self.inpainted = False

    @classmethod
    def from_segmenter(
        cls,
        image: Image.Image,
        labels: List[str],
        segmenter: ZeroShotSegmenter
    ) -> List['ImageSegment']:
        entities = segmenter(image, labels)
        segments = []
        for e in entities:
            box = Image.fromarray(e.mask).getbbox()
            xmin, ymin, xmax, ymax = box
            value = Image.new('RGBA', (xmax - xmin, ymax - ymin))
            value.paste(image.crop(box), (0, 0), Image.fromarray(e.mask))
            segment = cls(e.labels, e.score, segment)
            segment.move(xmin, ymin)
            segments.append(segment)

        return segments         
    

class Text(Graphic2D):
    def __init__(
        self, 
        content: str, 
        font_size: int = 10,
        font_weight: int = 1,
        font_family: str = '',
    ) -> None:
        super().__init__()
        self.content = content
        self.font_size = font_size
        self.font_weight = font_weight
        self.font_family = font_family

