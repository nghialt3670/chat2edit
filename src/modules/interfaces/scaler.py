import os, sys
sys.path.append(os.path.abspath(os.getcwd()))
from .base_module import MaskApplier
from src.cores.image_record import ImageRecord
from src.modules.engines.basic.process_image import scale_brightness, scale_contrast, scale_blurness, scale_sharpness


class Scaler(MaskApplier):

    def __init__(self, image_record: ImageRecord) -> None:
        super().__init__(image_record)


    def scale(self, category: str, target: str | None, factor: float) -> ImageRecord:
        result = self.image_record.create_next()
        scaled_image = None
        if category == "brightness": scaled_image = scale_brightness(result.image, factor)
        elif category == "contrast": scaled_image = scale_contrast(result.image, factor)
        elif category == "blurness": scaled_image = scale_blurness(result.image, factor)
        elif category == "sharpness": scaled_image = scale_sharpness(result.image, factor)
        else: raise ValueError(f"Unsupported category \"{category}\" for scale module")
        return self.apply_mask(result, target, scaled_image)

            
        
