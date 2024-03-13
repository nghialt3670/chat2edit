from typing import Tuple, List, Optional, Dict
from abc import ABC, abstractmethod
from PIL import Image

from .models import Graphic2D, BaseImage

class Canvas:
    def __init__(self, graphics: Optional[List[Graphic2D]] = None) -> None:
        self.graphics = graphics if graphics is not None else []

    def add(self, g: Graphic2D) -> None:
        self.graphics.append(g)

    def insert(self, i: int, g: Graphic2D) -> None:
        self.graphics.insert(i, g)

    def remove(self, g: Graphic2D) -> None:
        self.graphics.remove(g)

    def get_graphics_by_label(self, label: str) -> List[Graphic2D]:
        return [
            g for g in self.graphics 
            if hasattr(g, 'labels') and label in g.labels
        ]
    
    def get_graphic_by_uuid(self, uuid: str) -> Optional[Graphic2D]:
        for g in self.graphics:
            if g.uuid == uuid:
                return g
        
        return None
    
    def index_of(self, graphic: Graphic2D) -> int:
        return self.graphics.index(graphic) 
        
        