import numpy as np

from typing import List, Tuple, Optional, Dict, Set
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from PIL import Image
from uuid import uuid4

from .segmentation import ZeroShotSegmenter 
from .inpainting import ImageInpainter
from .utils import base64_encode, base64_decode

@dataclass
class GraphicProperties:
    uuid: str = str(uuid4()) 
    pos_x: int = 0
    pos_y: int = 0
    angle: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    flip_x: bool = False
    flip_y: bool = False
    brightness: float = 1.0
    contrast: float = 1.0
    blurness: float = 1.0
    temperature: float = 1.0


class Graphic(ABC):
    def __init__(
        self,
        members: Optional[List['Graphic']] = None,
        properties: Optional[GraphicProperties] = None
    ) -> None:
        self.members = members if members is not None else []
        self.properties = properties if properties is not None \
                          else GraphicProperties()

    def set_properties(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self.properties, key):
                setattr(self.properties, key, value)
    
    def move(
        self, 
        offsets: Tuple[int, int]
    ) -> None:
        self.properties.pos_x += offsets[0]
        self.properties.pos_x += offsets[1]
        for g in self.members:
            g.move(offsets)

    def rotate(
        self, 
        angle: float
    ) -> None:
        self.properties.angle += angle
        for g in self.members:
            g.rotate(angle)

    def scale(
        self,
        factors: Tuple[float, float]
    ) -> None:
        self.properties.scale_x *= factors[0]
        self.properties.scale_y *= factors[1]
        for g in self.members:
            g.scale(factors)

    def __eq__(
        self,
        g: 'Graphic'
    ) -> bool:
        return self.properties.uuid == g.properties.uuid
    
    def __hash__(self) -> int:
        return hash(self.properties.uuid)
    


class BasicImage(Graphic):
    def __init__(
        self, 
        value: Image.Image,
        members: Optional[List[Graphic]] = None,
        properties: Optional[GraphicProperties] = None
    ) -> None:
        super().__init__(members, properties)
        self.value = value

    @classmethod
    def from_base64(
        cls, 
        data: str
    ) -> 'BasicImage':
        return cls(base64_decode(data))
    
    def to_base64(self) -> str:
        return base64_encode(self.value)


class ImageInpaint(BasicImage):
    def __init__(
        self, 
        value: Image.Image, 
        members: Optional[List[Graphic]] = None,
        properties: Optional[GraphicProperties] = None
    ) -> None:
        super().__init__(value, members, properties)

    @classmethod
    def from_inpainter(
        cls, 
        image: Image.Image, 
        mask: np.ndarray,
        inpainter: ImageInpainter
    ) -> 'ImageInpaint':
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
        members: Optional[List[Graphic]] = None,
        properties: Optional[GraphicProperties] = None
    ) -> None:
        super().__init__(value, members, properties)
        self.labels = labels
        self.score = score

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
    

class Text(Graphic):
    def __init__(
        self, 
        content: str, 
        font_size: int = 10,
        font_weight: int = 1,
        font_family: str = '',
        members: Optional[List[Graphic]] = None,
        properties: Optional[GraphicProperties] = None
    ) -> None:
        super().__init__(members, properties)
        self.content = content
        self.font_size = font_size
        self.font_weight = font_weight
        self.font_family = font_family

