from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Dict

from PIL import Image
from io import BytesIO
from editor.utils import base64_decode
from editor.llm import OpenAILLM
from editor.inpainting import LaMaInpainter
from editor.segmentation import GroundingDINOSAM
from editor.editor import Editor
from editor.canvas import Canvas
from editor.wrapper import CanvasWrapper
from editor.graphic2d import (
    Graphic2D,
    BasicImage,
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

@app.post("/upload")
async def upload_image(requestBody: Dict):
    image_data = requestBody['data'].split(',')[1]
    image = base64_decode(image_data)
    basic_image = BasicImage(image)
    json_image = jsonable_encoder(basic_image.to_dict())
    return JSONResponse(content=json_image)


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request,}
    )


@app.post("/edit")
async def edit(request: Dict):
    mapping = {
        'uuid': 'uuid',
        'pos_x': 'left',
        'pos_y': 'top',
        'angle': 'angle',
        'scale_x': 'scaleX',
        'scale_y': 'scaleY',
        'flip_x': 'flipX',
        'flip_y': 'flipY',
    }
    objects = request['objects']
    instruction = request['instruction']

    canvas = Canvas()

    for obj in objects:
        if obj['category'] == 'basic-image':
            properties = {
                '_position': (obj['left'], obj['top']),
                '_rotation': float(obj['angle']),
                '_scale': (obj['scaleX'], obj['scaleY']),
                '_flip_x': bool(obj['flipX']),
                '_flip_y': bool(obj['flipY']),
                '_filters': obj['filters'],
            }

            data = obj['src'].split(',')[1]
            image = BasicImage.from_base64(data)
            image.set_properties(**properties)
            canvas.add(image)

    new_objects = []
    old_uuids = [obj['uuid'] for obj in objects]

    for i, g in enumerate(canvas.graphics):
        properties = {
            'left': g.position[0],
            'top': g.position[1],
            'angle': g.rotation,
            'scaleX': g.scale_x,
            'scaleY': g.scale_y,
            'flipX': g.flip_x,
            'flipY': g.flip_y,
            #TODO: implement filters
        }
        if g.uuid in old_uuids:
            objects[i].update(properties)
            objects[i]['new'] = 'false'
            new_objects.append(objects[i])
        else:
            new_obj = {}
            if isinstance(g, BasicImage):
                new_obj['src'] = 'data:image/jpeg;base64,' + g.base64_value()
            #TODO: implement other categories of graphic

            new_obj.update(properties)
            new_obj['new'] = 'true'
            new_objects.append(new_obj)

    response = {
        'fewshot': editor(canvas, instruction),
        'objects': new_objects
    }

    return JSONResponse(content=jsonable_encoder(response))