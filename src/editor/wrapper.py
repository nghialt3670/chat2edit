import numpy as np
from typing import Literal, Optional, List
from PIL import Image

from .canvas import Canvas
from .models import Graphic2D, ImageSegment, ImageInpaint
from .segmentation import ZeroShotSegmenter
from .inpainting import ImageInpainter


class CanvasWrapper:
    def __init__(
        self,
        canvas: Canvas,
        segmenter: ZeroShotSegmenter,
        inpainter: ImageInpainter
    ) -> None:
        self.canvas = canvas
        self.segmenter = segmenter
        self.inpainter = inpainter

    def find(self, prompt: str) -> List[ImageSegment]:
        graphics = self.canvas.get_graphics_by_label(prompt)
        if len(graphics) != 0:
            return graphics
    
        target_image = self.canvas.graphics[0].image
        return ImageSegment.from_segmenter(target_image, [prompt])
        
    def remove(self, targets: List[Graphic2D]) -> None:
        masks = [
            tar.get_mask() for tar in targets
            if isinstance(tar, ImageSegment) and not tar.inpainted
        ]
        combined_mask = np.maximum.reduce(masks)
        target_image = self.canvas.graphics[0].image
        inpaiting = ImageInpaint.from_inpainter(
            target_image, combined_mask, self.inpainter
        )
        self.canvas.insert(1, inpaiting)
        for tar in targets:
            self.canvas.remove(tar)

    def insert(self, entities: List[Graphic2D]) -> None:
        for g in entities:
            self.canvas.add(g)

    def replace(self, old: List[Graphic2D], new: Graphic2D) -> None:
        for g in old:
            i = self.canvas.index_of(old)
            new.properties.pos_x = g.properties.pos_x
            new.properties.pos_y = g.properties.pos_y
            self.canvas.set_graphic(i, new)

    def move(self, targets: List[Graphic2D], 
        x_offset: int, y_offset: int) -> None:
        for g in targets:
            i = self.canvas.index_of(g)
            g.move((x_offset, y_offset))
            self.canvas.set_graphic(i, g)

    def swap(self, entity1: Graphic2D, entity2: Graphic2D) -> None:
        i1 = self.canvas.index_of(entity1)
        i2 = self.canvas.index_of(entity2)
        self.canvas.set_graphic(i1, entity2)
        self.canvas.set_graphic(i2, entity1)
        
    def rotate(self, angle: float, direction: Literal['cw', 'ccw'], 
        target: Optional[Graphic2D] = None
        ) -> None:
        angle = angle if direction == 'cw' else angle * -1
        if target is not None:
            i = self.canvas.index_of(target)
            self.canvas.graphics[i].rotate(angle)
        else:
            self.canvas.graphics[0].rotate(angle)

    def flip(self, direction: Literal['vertical', 'horizontal'], 
        target: Optional[Graphic2D] = None
        ) -> None:
        i = self.canvas.index_of(target)

    def zoom(self, percent: float, target: Graphic2D) -> None:
        pass

    def convert(self, category: Literal['grayscale', 'negative'], target: Optional[Graphic2D] = None) -> None:
        pass