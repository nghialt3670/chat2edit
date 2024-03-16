import numpy as np
from typing import Literal, Optional, List

from .models import Graphic2D, ImageSegment
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

    def get_graphics_by_label(self, label) -> List[Graphic2D]:
        return [g for g in self.graphics if label in g.labels]

    def find(self, label: str) -> List[ImageSegment]:
        graphics = self.get_graphics_by_label(label)
        if len(graphics) != 0:
            return graphics

        segments = self.graphics[0].segment([label], self.segmenter)
        self.graphics.extend(segments)
        return segments
        
    def remove(self, graphics: List[Graphic2D]) -> None:
        for g in graphics: 
            self.graphics.remove(g)

        full_masks = [
            get_full_mask(
                g.get_mask(), 
                self.graphics[0].image.size[::-1], 
                (g.pos_x, g.pos_y)
            )
            for g in graphics 
            if isinstance(g, ImageSegment) and not g.inpainted
        ]
        combined_mask = np.maximum.reduce(full_masks)
        self.graphics[0].remove(combined_mask, self.inpainter)

    def insert(self, graphics: List[Graphic2D]) -> None:
        for g in graphics:
            self.graphics.append(g)

    def replace(self, graphics: List[Graphic2D], replacement: Graphic2D) -> None:
        for g in graphics:
            i = self.graphics.index(g)
            replacement.pos_x = g.pos_x
            replacement.pos_y = g.pos_y
            self.graphics[i] = replacement

    def move(self, graphics: List[Graphic2D], 
        x_offset: int, y_offset: int) -> None:
        for g in graphics:
            i = self.canvas.index_of(g)
            self.graphics[i].pos_x += x_offset
            self.graphics[i].pos_y += y_offset

    def swap(self, graphic1: Graphic2D, graphic2: Graphic2D) -> None:
        i1 = self.graphics.index(graphic1)
        i2 = self.graphics.index(graphic1)
        self.graphics[i1] = graphic2
        self.graphics[i2] = graphic1

    def rotate(self, angle: float, direction: Literal['cw', 'ccw'], 
        graphics: Optional[List[Graphic2D]] = None) -> None:
        angle = angle if direction == 'cw' else angle * -1
        if graphics is not None:
            for g in graphics:
                i = self.graphics.index(g)
                self.graphics[i].angle += angle
        else:
            self.graphics[0].angle += angle

    def flip(self, direction: Literal['vertical', 'horizontal'], 
        graphics: Optional[List[Graphic2D]] = None) -> None:
        if graphics is not None:
            for g in graphics:
                i = self.graphics.index(g)
                if direction == 'vertical':
                    self.graphics[i].flip_x = not self.graphics[i].flip_x
                else:
                    self.graphics[i].flip_y = not self.graphics[i].flip_y
        else:
            if direction == 'vertical':
                self.graphics[i].flip_x = not self.graphics[i].flip_x
            else:
                self.graphics[i].flip_y = not self.graphics[i].flip_y

    def zoom(self, percent: float, target: Graphic2D) -> None:
        pass

    def convert(self, category: Literal['grayscale', 'negative'], target: Optional[Graphic2D] = None) -> None:
        pass