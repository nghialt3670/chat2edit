from typing import Tuple, List, Optional, Dict
from abc import ABC, abstractmethod

from .graphic import Graphic


class Canvas:
    def __init__(
        self,
        graphics: Optional[List[Graphic]] = None
    ) -> None:
        self.graphics = graphics if graphics is not None else []

    def add(self, g: Graphic) -> None:
        self.graphics.append(g)

    def remove(self, g: Graphic) -> None:
        self.graphics.remove(g)

    def get_graphic_by_label(
        self, 
        label: str
    ) -> List[Graphic]:
        return [
            g for g in self.graphics 
            if hasattr(g, 'labels') and label in g.labels
        ]
    
    def get_graphic_by_uuid(
        self,
        uuid: str
    ) -> Optional[Graphic]:
        for g in self.graphics:
            if g.properties.uuid == uuid:
                return g
        
        return None
    
    def index_of(
        self,
        graphic: Graphic
    ) -> int:
        return self.graphics.index(graphic) 
            
    def set_graphic(
        self, 
        index: int,
        graphic: Graphic
    ) -> None:
        self.graphics[index] = graphic
        