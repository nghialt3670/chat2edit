import copy
import numpy as np
from PIL import Image
from typing import Literal, Optional, List

from .segmentation import ZeroShotSegmenter
from .inpainting import ImageInpainter
from .graphic import (
    Graphic, 
    BaseImage, 
    ImageSegment, 
    Text
)
from .utils import (
    get_full_mask,
    base64_decode, 
    base64_encode, 
    cut_image_from_mask
)

class Canvas:
    def __init__(
        self, 
        uid: str,
        graphics: List[Graphic],
        segmenter: Optional[ZeroShotSegmenter] = None, 
        inpainter: Optional[ImageInpainter] = None
    ) -> None:
        self.uid = uid
        self.graphics = graphics
        self.segmenter = segmenter
        self.inpainter = inpainter

    def set_models(
        self, 
        segmenter: ZeroShotSegmenter, 
        inpainter: ImageInpainter
    ) -> 'Canvas':
        self.segmenter = segmenter
        self.inpainter = inpainter
        return self
    
    def _segment(
        self, 
        image: Image.Image, 
        labels: List[str], 
        segmenter: ZeroShotSegmenter
    ) -> List['ImageSegment']:
        entities = segmenter(image, labels)
        segments = []
        for e in entities:
            xmin, ymin, _, _ = Image.fromarray(e.mask).getbbox()
            data = cut_image_from_mask(image, e.mask)
            segment = ImageSegment(data, e.score).shift((xmin, ymin)).label(e.labels)
            segments.append(segment)

        return segments 

    def find(self, prompt: str) -> List[Graphic]:
        graphics = [g for g in self.graphics if prompt in g.labels]
        if len(graphics) != 0:
            return graphics

        segments = self._segment(self.graphics[0].image, [prompt], self.segmenter)
        self.graphics.extend(segments)
        return segments
        
    def remove(self, graphics: List[Graphic]) -> None:
        for g in graphics: 
            self.graphics.remove(g)

        self._inpaint([g for g in graphics if isinstance(g, ImageSegment)])

    def insert(self, graphics: List[Graphic]) -> None:
        for g in graphics:
            self.graphics.append(g)

    def replace(self, graphics: List[Graphic], replacement: Graphic) -> None:
        for g in graphics:
            i = self.graphics.index(g)
            replacement.position = g.position
            self.graphics[i] = replacement

    def move(self, graphics: List[Graphic], x_offset: int, y_offset: int) -> None:
        self.remove(graphics)
        for g in graphics:
            self.graphics.append(g.shift((x_offset, y_offset)))

    def swap(self, graphic1: Graphic, graphic2: Graphic) -> None:
        i1 = self.graphics.index(graphic1)
        i2 = self.graphics.index(graphic1)
        self.graphics[i1] = graphic2
        self.graphics[i2] = graphic1

    def rotate(
        self, angle: float, 
        direction: Literal['cw', 'ccw'], 
        graphics: Optional[List[Graphic]] = None
    ) -> None:
        angle = angle if direction == 'cw' else angle * -1
        if graphics is not None:
            self._inpaint(self._filter_segment(graphics))
            for i in self._find_indices(graphics):
                self.graphics[i].rotate(angle)
        else:
            self.graphics[0].rotate(angle)

    def flip(
        self, 
        direction: Literal['vertical', 'horizontal'], 
        graphics: Optional[List[Graphic]] = None
    ) -> None:
        axis = 'x' if direction == 'horizontal' else 'y'
        if graphics is not None:
            self._inpaint(self._filter_segment(graphics))
            for i in self._find_indices(graphics):
                self.graphics[i].flip(axis)
        else:
            self.graphics[0].flip(axis)
                
    def zoom(self, percent: float, graphic: Graphic) -> None:
        pass

    def convert(
        self, 
        category: Literal['grayscale', 'negative'], 
        graphics: Optional[List[Graphic]] = None
    ) -> None:
        pass

    def _inpaint(self, segments: List[ImageSegment]) -> None:
        base_image = self.graphics[0].image

        full_masks = [
            get_full_mask(seg.mask, base_image.size, seg.position)
            for seg in segments if not seg.inpainted
        ]

        for i, g in enumerate(self.graphics):
            if g in segments:
                self.graphics[i].inpainted = True

        combined_mask = np.maximum.reduce(full_masks)
        self.graphics[0].image = self.inpainter(base_image, combined_mask)

    def _find_indices(self, graphics: List[Graphic]) -> List[int]:
        graphic_set = set(graphics)
        return [i for i, g in enumerate(self.graphics) if g in graphic_set]
    



        
