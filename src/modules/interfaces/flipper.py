import os, sys
sys.path.append(os.path.abspath(os.getcwd()))

from typing import Literal
from .base_module import SpaceTransformer
from src.cores.image_record import ImageRecord
from src.modules.engines.basic.process_image import vertical_flip, horizontal_flip



class Flipper(SpaceTransformer):

    def __init__(self, image_record: ImageRecord) -> None:
        super().__init__(image_record)


    def flip(self, direction: Literal["vertical", "horizontal"]) -> ImageRecord:
        if direction is None: direction = "horizontal"
        result = self.image_record.create_next()
        if direction == "vertical": return self.transform(result, vertical_flip)
        if direction == "horizontal": return self.transform(result, horizontal_flip)
        raise ValueError(f"Unsupported direction \"{direction}\" for flip module")
            
        
