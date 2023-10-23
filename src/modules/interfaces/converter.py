import os, sys
sys.path.append(os.path.abspath(os.getcwd()))

from .base_module import MaskApplier
from src.cores.image_record import ImageRecord
from src.modules.engines.basic.process_image import convert_to_negative, convert_to_grayscale



class Converter(MaskApplier):

    def __init__(self, image_record: ImageRecord) -> None:
        super().__init__(image_record)


    def convert(self, category: str, target: str | None) -> ImageRecord:
        result = self.image_record.create_next()
        converted_image = None
        if category == "grayscale": converted_image = convert_to_grayscale(result.image)
        elif category == "negative": converted_image = convert_to_negative(result.image)
        else: raise ValueError(f"Unsupported category \"{category}\" for convert module")
        return self.apply_mask(result, target, converted_image)

            
        
