const editBtn = document.getElementById('editBtn');


editBtn.onclick = async (e) => {
    e.preventDefault();
    const instruction = document.getElementById('instruction');
    const endpoint = '/edit';

    if (instruction.value.trim() == '') {
        alert('Please give your instruction to edit the image')
        return
    }

    const graphics = canvas.getObjects().map((obj) => {
        obj = obj.toJSON(['labels', 'uuid', 'category']);
        let graphicAttributes = {
            labels: obj.labels,
            uuid: obj.uuid,
            category: obj.category,
            pos_x: obj.left,
            pos_y: obj.top,
            angle: obj.angle,
            scale_x: obj.scaleX,
            scale_y: obj.scaleY,
            flip_x: obj.flipX,
            flip_y: obj.flipY,
            filters: obj.filters,
        }
        if (obj.category == 'base-image') {
            return {
                ...graphicAttributes,
                base64_str: toBase64Str(obj.src),
            }
        } else if (obj.category == 'image-segment') {
            return {
                ...graphicAttributes,
                base64_str: toBase64Str(obj.src),
                score: obj.score,
                inpainted: obj.inpainted,
            }
        }
    });

    console.log(graphics)

    requestBody = JSON.stringify(graphics);

    request = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: requestBody,
    }

    param = new URLSearchParams({instruction: instruction.value})
    parameterized_endpoint = endpoint + '?' + param

    const response = await fetch(parameterized_endpoint, request);
    const data = await response.json();
    const newGraphics = data['graphics'];
    const oldObjects = canvas.getObjects().map((obj) => obj.toJSON(['uuid', 'category']));
    const newObjects = newGraphics.map((graphic) => {
        let attributes = {
            labels: graphic.labels,
            uuid: graphic.uuid,
            category: graphic.category,
            left: graphic.pos_x,
            top: graphic.pos_y,
            angle: graphic.angle,
            scaleX: graphic.scale_x,
            scaleY: graphic.scale_y,
            flipX: graphic.flip_x,
            flipY: graphic.flip_y,
            filters: graphic.filters,
        }
        if (graphic.category === 'base-image') {
            attributes = {
                ...attributes, 
                src: toBase64Url(graphic.base64_str),
                selectable: false,
                hoverCursor: "mouse"
            }
        } else if (graphic.category === 'image-segment') {
            attributes = {
                ...attributes,
                src: toBase64Url(graphic.base64_str),
                score: graphic.score,
                inpainted: graphic.inpainted,
            }
        }
        const idx = oldObjects.findIndex((obj) => {
            return obj.uuid === graphic.uuid
        });
        if (idx != -1) {
            return { ...oldObjects[idx], ...attributes, };
        } else {
            const image = new fabric.Image('');
            return { ...image.toJSON(), ...attributes };          
        }
    });

    // console.log(newObjects)
    // console.log(oldObjects)

    fabric.util.enlivenObjects(newObjects, function(objects) {
        canvas.renderOnAddRemove = false;
        canvas.clear();

        objects.forEach((o, i) => {
            canvas.insertAt(o, i);
        });
      
        canvas.renderOnAddRemove = true;
        canvas.renderAll();
    });
}


