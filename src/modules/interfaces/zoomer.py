import os, sys
sys.path.append(os.path.abspath(os.getcwd()))

import numpy as np
from .base_module import SpaceTransformer
from src.cores.image_record import ImageRecord, EditStatus
from src.modules.engines.basic.process_image import zoom


class Zoomer(SpaceTransformer):

    def __init__(self, image_record: ImageRecord) -> None:
        super().__init__(image_record)


    def zoom(self, factor: float, target: str | None) -> ImageRecord:
        result = self.image_record.create_next()

        if target is None:
            pivot = (result.image.shape[1] // 2, result.image.shape[0] // 2)
            return self.transform(result, zoom, factor, pivot)

        self.detect(result, target)

        if target not in result.bboxes:
            result.edit_status = EditStatus.TARGET_NOT_FOUND
            return result
        
        xmin, ymin, xmax, ymax = result.bboxes[target] 
        pivot = (int((ymin + ymax) // 2), int((xmin + xmax) // 2))
        return self.transform(result, zoom, factor, pivot)
    




        

            
        
