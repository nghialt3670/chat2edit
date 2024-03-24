from .canvas import Canvas
from .dtos import CanvasDTO, GraphicDTO, TextDTO, BaseImageDTO, ImageSegmentDTO
from .graphic import Graphic, Text, BaseImage, ImageSegment, Transform


class CanvasMapper:
    @classmethod
    def to_dto(cls, canvas: Canvas) -> CanvasDTO:
        graphic_dtos = []
        for graphic in canvas.graphics:
            props = {
                'uid': graphic.uid,
                'labels': graphic.labels,
                'category': 'base-image',
            }
            props.update(vars(graphic.transform))
            dto = None
            if isinstance(graphic, BaseImage):
                dto = BaseImageDTO(
                    **props,
                    base64=graphic.base64,
                    filters=graphic.filters
                )
            elif isinstance(graphic, ImageSegment):
                dto = ImageSegmentDTO(
                    **props,
                    base64=graphic.base64,
                    filters=graphic.filters,
                    score=graphic.score,
                    inpainted=graphic.inpainted,
                )
            elif isinstance(graphic, Text):
                dto = TextDTO(
                    **props,
                    content=graphic.content,
                    font_family=graphic.font_family,
                    font_style=graphic.font_style,
                    font_size=graphic.font_size,
                    font_weight=graphic.font_weight
                )

            graphic_dtos.append(dto)

        return CanvasDTO(uid=canvas.uid, graphics=graphic_dtos)
    
    @classmethod
    def from_dto(cls, canvas_dto: CanvasDTO) -> Canvas:
        graphics = []
        for dto in canvas_dto.graphics:
            graphic = None
            props = {
                'uid': dto.uid,
                'labels': dto.labels,
                'transform': Transform(
                    pos_x=dto.pos_x,
                    pos_y=dto.pos_y,
                    scale_x=dto.scale_y,
                    scale_y=dto.scale_y,
                    flip_x=dto.flip_x,
                    flip_y=dto.flip_y,
                    rotation= dto.rotation
                )
            } 
            if isinstance(dto, BaseImageDTO):
                graphic = BaseImage(
                    data=dto.base64,
                    filters=dto.filters,
                    **props
                )
            if isinstance(dto, ImageSegmentDTO):
                graphic = ImageSegment(
                    data=dto.base64,
                    score=dto.score,
                    inpainted=dto.inpainted,
                    filters=dto.filters,
                    **props
                )
            if isinstance(dto, TextDTO):
                graphic = Text(
                    content=dto.content,
                    font_family=dto.font_family,
                    font_style=dto.font_style,
                    font_size=dto.font_size,
                    font_weight=dto.font_weight
                )
            graphics.append(graphic)

        return Canvas(canvas_dto.uid, graphics)

