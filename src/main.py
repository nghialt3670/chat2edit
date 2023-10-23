import os, sys
sys.path.append(os.path.abspath(os.getcwd()))

import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO
from cores.interpreter import Interpreter
from cores.generator import OpenAIGenerator
from utils.config_manager import ConfigManager
from utils.read_txt import read_txt
import sys
import os


CONFIG_FILE_PATH = "config.yaml"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") 


config_manager = ConfigManager(CONFIG_FILE_PATH)

OPENAI_MODEL_NAME = config_manager.get("openai_model_name")
FEWSHOT_FILE_PATH = config_manager.get("fewshot_file_path")
INIT_VARNAME = config_manager.get("initial_varname")
FEWSHOT_PROMPT = read_txt(FEWSHOT_FILE_PATH)

generator = OpenAIGenerator(model=OPENAI_MODEL_NAME, api_key=OPENAI_API_KEY)
interpreter = Interpreter(init_varname=INIT_VARNAME)


def edit(image: np.ndarray, instruction: str) -> np.ndarray:
    prompt = FEWSHOT_PROMPT.replace("{***}", instruction)
    program = generator.generate(prompt)
    print(program)
    result = interpreter.interpret(image, program)
    interpreter.reset()
    print(result.edit_status)
    return result.image


@st.cache_data
def get_pil_image(image: np.ndarray):
    pil_image = Image.fromarray(image)
    return pil_image


@st.cache_data
def get_image_bytes(image: np.ndarray, format: str) -> BytesIO:
    img_byte_array = BytesIO()
    pil_image = get_pil_image(image)
    pil_image.save(img_byte_array, format=format)
    img_byte_array.seek(0)
    return img_byte_array

def main():
    st.set_page_config(
        page_title="Chat2Edit",
        page_icon="hehe",
        layout="wide"
    )

    title_html = """<h1 style='text-align: center;'>CHAT2EDIT</h1>"""
    subtitle_html = """<h5 style='text-align: center;'>MMLAB - UIT - VNU HCM</h5>"""
    st.markdown(title_html, unsafe_allow_html=True)
    st.markdown(subtitle_html, unsafe_allow_html=True)


    uploaded_image = st.file_uploader("", type=["jpg", "png", "jpeg"])

    left_column, right_column = st.columns(2)
    instruction = None

    if uploaded_image is not None:
        instruction = st.text_input("")
        with left_column:
            image = Image.open(uploaded_image)
            st.image(image, use_column_width=True)
            image = np.array(image)
        
        if st.button("Submit"):
            if instruction == "":
                st.warning("You must provide instructions before submitting!")
                return
            with right_column:
                result_image = edit(image, instruction)
                st.image(get_pil_image(result_image), use_column_width=True)

            # st.download_button(
            #     label="Download",
            #     data=get_image_bytes(result_image, format="PNG"),
            #     file_name="processed_image.png",
            # )


if __name__ == "__main__":
    main()