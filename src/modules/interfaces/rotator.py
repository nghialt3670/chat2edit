import os, sys
sys.path.append(os.path.abspath(os.getcwd()))

from typing import Literal
from .base_module import SpaceTransformer
from src.cores.image_record import ImageRecord
from src.modules.engines.basic.process_image import rotate_clockwise, rotate_counter_clockwise



class Rotator(SpaceTransformer):

    def __init__(self, image_record: ImageRecord) -> None:
        super().__init__(image_record)


    def rotate(self, angle: float, direction: Literal["clockwise", "counter-clockwise"] | None) -> ImageRecord:
        result = self.image_record.create_next()
        if direction is None: direction = "clockwise"
        if direction == "clockwise": return self.transform(result, rotate_clockwise, angle)
        if direction == "counter-clockwise": return self.transform(result, rotate_counter_clockwise, angle)
        raise ValueError(f"Unsupported direction \"{direction}\" for rotate module")
            
        
