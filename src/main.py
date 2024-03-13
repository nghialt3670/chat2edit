from fastapi import FastAPI, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Dict, List, Union

from PIL import Image
from io import BytesIO
from editor.utils import base64_decode
from editor.llm import OpenAILLM
from editor.inpainting import LaMaInpainter
from editor.segmentation import GroundingDINOSAM
from editor.editor import Editor
from editor.canvas import Canvas
from editor.wrapper import CanvasWrapper
from editor.models import (
    Graphic2D,
    BaseImage,
    TargetImage,
    ImageInpaint,
    ImageSegment,
    Text
)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# segmenter = GroundingDINOSAM(
#     gd_model_path='./static/pretrained/groundingdino_swint_ogc.pth',
#     gd_config_path='./config/GroundingDINO_SwinT_OGC.py',
#     sam_model_path='./static/pretrained/sam_vit_b_01ec64.pth',
#     sam_model_type='vit_b'
# )
# inpainter = LaMaInpainter(
#     model_path='./static/pretrained/big-lama.pt',
#     device='cpu'
# )
llm = OpenAILLM('')
editor = Editor(
    segmenter=None, 
    inpainter=None, 
    llm=llm,
    wrapper=CanvasWrapper(None, None, None)
)


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request,}
    )


@app.post("/edit")
async def edit(
    instruction: str,
    graphics: List[Union[BaseImage, ImageInpaint, ImageSegment, Text, TargetImage]] = Body(...)
) -> JSONResponse:
    canvas = Canvas(graphics)
    canvas = editor(canvas, instruction)
    response = {
        'graphics': canvas.graphics
    }

    return JSONResponse(content=jsonable_encoder(response))


