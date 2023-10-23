import os, sys
sys.path.append(os.path.abspath(os.getcwd()))

from typing import Any, Dict, List
import re
import numpy as np
from .image_record import ImageRecord
from src.modules.interfaces.scaler import Scaler
from src.modules.interfaces.converter import Converter
from src.modules.interfaces.eraser import Eraser
from src.modules.interfaces.rotator import Rotator
from src.modules.interfaces.flipper import Flipper
from src.modules.interfaces.zoomer import Zoomer
from src.utils.checktype import is_int_format, is_float_format, is_string_format


class Interpreter:
    def __init__(self, init_varname: str) -> None:
        self.context = {}
        self.init_varname = init_varname


    def interpret(self, image: np.ndarray, program) -> ImageRecord:
        image_record = ImageRecord(image)
        self.context[self.init_varname] = image_record
        steps = self.parse_program(program)

        for step in steps:
            varname, module, args_dict = self.parse_step(step)
            self.context[varname] = self.call_module(module, args_dict)

        return self.result()


    def call_module(self, module: str, args_dict: dict) -> np.ndarray:
        if module == "scale":
            arg_names = ["image", "category", "factor", "target"]
            image, category, factor, target = self.get_arg_values(args_dict, arg_names)
            return Scaler(self.context[image]).scale(category, target, factor)
        
        if module == "convert":
            arg_names = ["image", "category", "target"]
            image, category, target = self.get_arg_values(args_dict, arg_names)
            return Converter(self.context[image]).convert(category, target)
        
        if module == "erase":
            arg_names = ["image", "target"]
            image, target = self.get_arg_values(args_dict, arg_names)
            return Eraser(self.context[image]).erase(target)
        
        if module == "rotate":
            arg_names = ["image", "angle", "direction"]
            image, angle, direction = self.get_arg_values(args_dict, arg_names)
            return Rotator(self.context[image]).rotate(angle, direction)
        
        if module == "flip":
            arg_names = ["image", "direction"]
            image, direction = self.get_arg_values(args_dict, arg_names)
            return Flipper(self.context[image]).flip(direction)
        
        if module == "zoom":
            arg_names = ["image", "factor", "target"]
            image, factor, target = self.get_arg_values(args_dict, arg_names)
            return Zoomer(self.context[image]).zoom(factor, target) 
        
        raise ValueError("Unsupported module \"{module}\"")


    def get_arg_values(sefl, args_dict: Dict[str, int | float | str], arg_names: List[str]) -> List[Any]:
        return [args_dict[arg_name] if arg_name in args_dict else None
                for arg_name in arg_names]


    def result(self) -> ImageRecord:
        return list(self.context.values())[-1]
    


    def reset(self) -> None:
        self.context = {}



    def format_step(self, step: str) -> str:
        return step.strip()
    

    
    def parse_module_args(self, tokens: list[str]) -> list:
        args_dict = {tokens[i]:tokens[i + 1] for i in range(0, len(tokens) - 1, 2)}

        for name, val in args_dict.items():
            if is_string_format(val): args_dict[name] = val[1:-1]
            elif is_float_format(val): args_dict[name] = float(val)
            elif is_int_format(val): args_dict[name] = int(val)
            else: args_dict[name] = val

        return args_dict


    def parse_step(self, line: str) -> list[str]:
        delimiter_chars = ",=()"
        tokens = re.split('[' + re.escape(delimiter_chars) + ']', line)[:-1]
        tokens = [token.strip() for token in tokens]
        args_dict = self.parse_module_args(tokens[2:])
        step_info = [tokens[0], tokens[1], args_dict]
        return step_info


    def parse_program(self, program: str) -> list[str]:
        program = program.strip()
        steps = program.split("\n")
        steps = [self.format_step(step) for step in steps if step != ""]
        return steps