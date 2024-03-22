from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union

from editor.llm import OpenAILLM
from editor.inpainting import LaMaInpainter
from editor.segmentation import GroundingDINOSAM
from editor.editor import Editor
from editor.canvas import Canvas
from editor.graphic2d import (
    BaseImage,
    ImageSegment,
    Text
)


app = FastAPI()


origins = [
    "http://localhost:5173",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)



segmenter = GroundingDINOSAM(
    gd_model_path='./pretrained/groundingdino_swint_ogc.pth',
    gd_config_path='./config/GroundingDINO_SwinT_OGC.py',
    sam_model_path='./pretrained/sam_vit_b_01ec64.pth',
    sam_model_type='vit_b'
)

inpainter = LaMaInpainter(
    model_path='./pretrained/big-lama.pt',
    device='cpu'
)

llm = OpenAILLM('')
editor = Editor(
    llm=llm,
)

@app.post("/edit")
async def edit(
    instruction: str,
    graphics_list: List[List[Union[BaseImage, ImageSegment, Text]]] = Body(...)
) -> JSONResponse:
    canvases = [Canvas(graphics, segmenter, inpainter) for graphics in graphics_list]
    edited_canvases = editor(canvases, instruction)
    response = {
        'graphics_list': [canvas.graphics for canvas in edited_canvases] 
    }

    return JSONResponse(content=jsonable_encoder(response))