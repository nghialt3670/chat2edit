from typing import List

from .segmentation import ZeroShotSegmenter
from .inpainting import ImageInpainter
from .llm import LLM

from .base_program import BASE_PROGRAM_1
from .canvas import Canvas
from .canvas import Graphic


class Editor:
    def __init__(
        self,
        segmenter: ZeroShotSegmenter,
        inpainter: ImageInpainter,
        llm: LLM,
    ) -> None:
        self.segmenter = segmenter
        self.inpainter = inpainter
        self.llm = llm

    def __call__(
        self, 
        canvas: Canvas,
        instruction: str
    ) -> Canvas:
        


        return canvas
    


