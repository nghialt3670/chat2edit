from __future__ import annotations
import numpy as np
from enum import Enum 
from typing import Dict


class ImageRecord:

    def __init__(self, image: np.ndarray, prev_record: ImageRecord | None = None,
                 next_record: ImageRecord | None = None, masks: Dict[str, np.ndarray] = {},
                 bboxes: Dict[str, np.ndarray] = {}, edit_status: EditStatus | None = None) -> None:
        
        self.image = image
        self.prev_record = prev_record
        self.next_record = next_record
        self.masks = masks
        self.bboxes = bboxes
        self.edit_status = edit_status
    

    def create_next(self) -> ImageRecord:
        next_record = ImageRecord(
            prev_record=self,
            image=self.image.copy(),
            masks=self.masks.copy(),
            bboxes=self.bboxes.copy()
        )
        self.next_record = next_record
        return next_record



class EditStatus(Enum):
    SUCCESS = 0
    TARGET_NOT_FOUND = 1

