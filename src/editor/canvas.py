from typing import Tuple, List, Optional, Dict
from abc import ABC, abstractmethod

from .graphic2d import Graphic2D


class Canvas:
    def __init__(
        self,
        graphics: Optional[List[Graphic2D]] = None
    ) -> None:
        self._graphics = graphics if graphics is not None else []

    @property
    def graphics(self) -> List[Graphic2D]:
        return self._graphics.copy()

    def add(self, g: Graphic2D) -> None:
        self._graphics.append(g)

    def insert(self, i: int, g: Graphic2D) -> None:
        self._graphics.insert(i, g)

    def remove(self, g: Graphic2D) -> None:
        self._graphics.remove(g)

    def set_graphic(self, i: int, g: Graphic2D) -> None:
        self._graphics[i] = g

    def get_graphics_by_label(self, label: str) -> List[Graphic2D]:
        return [
            g for g in self._graphics 
            if hasattr(g, 'labels') and label in g.labels
        ]
    
    def get_graphic_by_uuid(self, uuid: str) -> Optional[Graphic2D]:
        for g in self._graphics:
            if g.uuid == uuid:
                return g
        
        return None
    
    def index_of(self, graphic: Graphic2D) -> int:
        return self._graphics.index(graphic) 
        
        