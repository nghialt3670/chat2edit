from typing import Literal, Optional, List

from .canvas import Canvas
from .graphic import Graphic

class CanvasWrapper:
    def __init__(
        self,
        canvas: Canvas
    ) -> None:
        self.canvas = canvas

    def find(self, prompt: str) -> List[Graphic]:
        graphics = self.canvas.get_graphic_by_label(prompt)

    
    def remove(self, targets: List[Graphic]) -> None:
        for g in targets:
            self.canvas.remove(g)

    def insert(self, entities: List[Graphic]) -> None:
        for g in entities:
            self.canvas.add(g)

    def replace(self, olds: List[Graphic], new: Graphic) -> None:
        for g in olds:
            i = self.canvas.index_of(olds)
            new.properties.pos_x = g.properties.pos_x
            new.properties.pos_y = g.properties.pos_y
            self.canvas.set_graphic(i, new)

    def move(self, targets: List[Graphic], x_offset: int, y_offset: int) -> None:
        for g in targets:
            i = self.canvas.index_of(g)
            g.move((x_offset, y_offset))
            self.canvas.set_graphic(i, g)

    def swap(self, entity1: Graphic, entity2: Graphic) -> None:
        i1 = self.canvas.index_of(entity1)
        i2 = self.canvas.index_of(entity2)
        self.canvas.set_graphic(i1, entity2)
        self.canvas.set_graphic(i2, entity1)
        

    def rotate(self, angle: float, direction: Literal['cw', 'ccw'], target: Optional[Graphic] = None) -> None:
        angle = angle if direction = 'cw' else angle * -1
        if target is not None:
            target.rotate(angle)
            i = self.canvas.index_of(target)
            self.canvas.set_graphic(i, target)
        else:
            self.canvas.set_graphic(0, self.canvas.graphics[0].rotate(angle))
        


    def flip(direction: Literal['vertical', 'horizontal'], target: Optional[Graphic] = None) -> None:
        

    def zoom(percent: float, target: Graphic) -> None:
        pass

    def convert(category: Literal['grayscale', 'negative'], target: Optional[Graphic] = None) -> None:
        pass



