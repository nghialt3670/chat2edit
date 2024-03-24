from pydantic import BaseModel
from typing import List, Union, Set, Tuple


class FilterDTO(BaseModel):
    name: str
    value: float


class GraphicDTO(BaseModel):
    uid: str 
    labels: Set[str]
    category: str
    pos_x: int 
    pos_y: int 
    rotation: float 
    scale_x: float 
    scale_y: float 
    flip_x: bool 
    flip_y: bool 
    

class BaseImageDTO(GraphicDTO):
    base64: str
    filters: List[FilterDTO] 


class ImageSegmentDTO(BaseImageDTO):
    score: float
    inpainted: bool


class TextDTO(GraphicDTO):
    content: str
    font_family: str
    font_style: str
    font_size: Union[str, int]
    font_weight: Union[str, int]


class CanvasDTO(BaseModel):
    uid: str
    graphics: List[Union[BaseImageDTO, ImageSegmentDTO, TextDTO]]
    