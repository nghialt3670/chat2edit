import os, sys
sys.path.append(os.path.abspath(os.getcwd()))

from .base_module import MaskApplier
from src.cores.image_record import ImageRecord
from src.modules.engines.basic.process_image import erase



class Eraser(MaskApplier):

    def __init__(self, image_record: ImageRecord) -> None:
        super().__init__(image_record)


    def erase(self, target: str | None) -> ImageRecord:
        result = self.image_record.create_next()
        erased_image = erase(result.image)
        return self.apply_mask(result, target, erased_image)

            
        
