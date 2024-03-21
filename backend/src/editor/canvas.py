import copy
import numpy as np
from PIL import Image
from typing import Literal, Optional, List, Type

from .graphic2d import Graphic2D, ImageSegment
from .segmentation import ZeroShotSegmenter
from .inpainting import ImageInpainter
from .utils import get_full_mask


class Canvas:
    def __init__(
        self,
        graphics: List[Graphic2D],
        segmenter: ZeroShotSegmenter,
        inpainter: ImageInpainter
    ) -> None:
        self.graphics = graphics
        self.segmenter = segmenter
        self.inpainter = inpainter

    def find(self, prompt: str) -> List[Graphic2D]:
        graphics = [g for g in self.graphics if prompt in g.labels]
        if len(graphics) != 0:
            return graphics

        segments = self.graphics[0].segment([prompt], self.segmenter)
        self.graphics.extend(segments)
        return segments
        
    def remove(self, graphics: List[Graphic2D]) -> None:
        for g in graphics: 
            self.graphics.remove(g)

        segments = self._filter_segment(graphics)
        self._inpaint(segments)

    def insert(self, graphics: List[Graphic2D]) -> None:
        for g in graphics:
            self.graphics.append(g)

    def replace(self, graphics: List[Graphic2D], replacement: Graphic2D) -> None:
        for g in graphics:
            i = self.graphics.index(g)
            replacement.position = g.position
            self.graphics[i] = replacement

    def move(self, graphics: List[Graphic2D], x_offset: int, y_offset: int) -> None:
        self.remove(graphics)
        for g in graphics:
            g.move((x_offset, y_offset))
            self.graphics.append(g)

    def swap(self, graphic1: Graphic2D, graphic2: Graphic2D) -> None:
        i1 = self.graphics.index(graphic1)
        i2 = self.graphics.index(graphic1)
        self.graphics[i1] = graphic2
        self.graphics[i2] = graphic1

    def rotate(self, angle: float, direction: Literal['cw', 'ccw'], graphics: Optional[List[Graphic2D]] = None) -> None:
        angle = angle if direction == 'cw' else angle * -1
        if graphics is not None:
            self._inpaint(self._filter_segment(graphics))
            for i in self._find_indices(graphics):
                self.graphics[i].rotate(angle)
        else:
            self.graphics[0].rotate(angle)

    def flip(self, direction: Literal['vertical', 'horizontal'], graphics: Optional[List[Graphic2D]] = None) -> None:
        axis = 'x' if direction == 'horizontal' else 'y'
        if graphics is not None:
            self._inpaint(self._filter_segment(graphics))
            for i in self._find_indices(graphics):
                self.graphics[i].flip(axis)
        else:
            self.graphics[0].flip(axis)
                
    def zoom(self, percent: float, graphic: Graphic2D) -> None:
        pass

    def convert(self, category: Literal['grayscale', 'negative'], graphics: Optional[List[Graphic2D]] = None) -> None:
        pass

    def _filter_segment(self, graphics: List[Graphic2D]) -> List[ImageSegment]:
        return [g for g in graphics if isinstance(g, ImageSegment)]

    def _inpaint(self, segments: List[ImageSegment]) -> None:
        base_image = self.graphics[0].image

        full_masks = [
            get_full_mask(seg.get_mask(), base_image.size, seg.position)
            for seg in segments if not seg.inpainted
        ]

        for i, g in enumerate(self.graphics):
            if g in segments:
                self.graphics[i].inpainted = True

        combined_mask = np.maximum.reduce(full_masks)
        Image.fromarray(combined_mask).save('combined_mask.png')
        self.graphics[0].image = self.inpainter(base_image, combined_mask)
        self.graphics[0].image.save('inpainted.png')

    def _find_indices(self, graphics: List[Graphic2D]) -> List[int]:
        graphic_set = set(graphics)
        return [i for i, g in enumerate(self.graphics) if g in graphic_set]


        
