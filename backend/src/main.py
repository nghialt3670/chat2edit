from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from editor.llm import OpenAILLM
from editor.inpainting import LaMaInpainter
from editor.segmentation import GroundingDINOSAM
from editor.editor import Editor
from editor.dtos import CanvasDTO
from editor.mapper import CanvasMapper

 
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
    canvases: List[CanvasDTO] = Body(...)
) -> JSONResponse:
    canvases = [CanvasMapper.from_dto(canvas).set_models(segmenter, inpainter) for canvas in canvases]
    canvases = editor(canvases, instruction)
    response = {
        'canvases': [CanvasMapper.to_dto(canvas) for canvas in canvases]
    }

    return JSONResponse(content=jsonable_encoder(response))