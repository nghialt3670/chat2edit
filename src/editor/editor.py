import inspect
import re
from typing import List, Dict

from .segmentation import ZeroShotSegmenter
from .inpainting import ImageInpainter
from .llm import LLM
from .canvas import Canvas
from .graphic2d import Graphic2D
from .wrapper import CanvasWrapper

class Editor:
    def __init__(
        self,
        segmenter: ZeroShotSegmenter,
        inpainter: ImageInpainter,
        llm: LLM,
        wrapper: CanvasWrapper,
    ) -> None:
        self.segmenter = segmenter
        self.inpainter = inpainter
        self.llm = llm
        self.wrapper = wrapper

    def __call__(
        self, 
        canvas: Canvas,
        instruction: str
    ) -> Canvas:
        prompt = self._create_prompt(instruction)
        program = self.llm(prompt)
        function = self._get_function_string(program)
        mappings = {
            'Image': 'CanvasWrapper',
            'Entity': 'Graphic2D',
        }
        function = self._replace(function, mappings)

        exec(function, globals())
        # return process_image(canvas)
        return canvas
    
    def _get_function_string(self, text: str) -> str:
        return text[text.find('def'):text.find('```')]

    
    def _create_prompt(self, instruction: str) -> str:
        class_type = self.wrapper.__class__
        prompt = 'Suppose you have this implemeted class:\n'
        prompt += f'class {class_type.__name__}:\n' 
        for declaration in self._get_function_declarations(class_type):
            prompt += f'\t{declaration}\n'

        prompt += f'\nImplement the function below to satisfy the instruction: {instruction}\n'
        prompt += 'Note: Just give the function implementation, dont give explainations or anything else.'
        prompt += '\ndef process_image(image: Image) -> Image:\n'
        prompt += '\t# Your implementation\n'
        mappings = {
            'CanvasWrapper': 'Image',
            'Graphic2D': 'Entity',
            'ImageSegment': 'Entity'
        }
        return self._replace(prompt, mappings)

    def _replace(self, prompt: str, mappings: Dict) -> str:
        for k, v in mappings.items():
            prompt = prompt.replace(k, v)

        return prompt

    def _get_function_declarations(self, class_type) -> List[str]:
        function_declarations = []
        for name, member in inspect.getmembers(class_type):
            if inspect.isfunction(member):
                source_lines, _ = inspect.getsourcelines(member)
                signature = ''.join(source_lines).strip()
                return_type = re.search(r'->\s*([^:\s]+)', signature)
                if return_type:
                    return_type = return_type.group(1)
                else:
                    return_type = 'None'
                function_declaration = re.search(r'def\s+.*?\(.*?\)', signature)
                if function_declaration:
                    function_signature = function_declaration.group() + ' -> ' + return_type
                    function_declarations.append(function_signature)
        return function_declarations


    


