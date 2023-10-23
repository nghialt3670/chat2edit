import re
import yaml 


def is_string_format(input: str) -> bool:
    return (input.startswith("\"") and input.endswith("\"")) or \
           (input.startswith("'") and input.endswith("'"))


def is_int_format(input: str) -> bool:
    try:
        input = int(input)
        return True
    except:
        return False
    

def is_float_format(input: str) -> bool:
    try: 
        input = float(input)
        return True
    except: 
        return False
    

def txt_to_str(fewshot_file_path: str) -> str:
    with open(fewshot_file_path, "r", encoding="utf-8") as file:
        file_contents = file.read()

    return file_contents
