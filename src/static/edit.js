const editBtn = document.getElementById('editBtn');


editBtn.onclick = async (e) => {
    const instruction = document.getElementById('instruction');
    const endpoint = '/edit';

    if (instruction.value.trim() == '') {
        alert('Please give your instruction to edit the image')
        return
    }

    const graphics = canvas.getObjects().map((obj) => {
        obj = obj.toJSON(['uuid', 'category']);
        if (obj.category == 'target-image') {
            return {
                uuid: obj.uuid,
                category: obj.category,
                pos_x: obj.left,
                pos_y: obj.top,
                angle: obj.angle,
                scale_x: obj.scaleX,
                scale_y: obj.scaleY,
                filters: obj.filters,
                base64_str: obj.src,
                members: obj.members
            }
        } else {

        }
    });

    requestBody = JSON.stringify(graphics);
    console.log(requestBody)
    request = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: requestBody,
    }

    param = new URLSearchParams({instruction: instruction.value})
    parameterized_endpoint = endpoint + '?' + param

    const response = await fetch(parameterized_endpoint, request);
    const data = await response.json();
    const new_graphics = data['graphics'];
    const old_objects = canvas.toJSON().objects;
    const new_objects = new_graphics.map((graphic) => {
        if (graphic.category === 'target-image') {
            obj_attributes = {
                uuid: graphic.uuid,
                category: graphic.category,
                left: graphic.pos_x,
                top: graphic.pos_y,
                angle: graphic.angle,
                scaleX: graphic.scale_x,
                scaleY: graphic.scale_y,
                filters: graphic.filters,
                src: graphic.base64_str,
                members: graphic.members
            }
            const idx = old_objects.findIndex((obj) => (obj.uuid == graphic.uud));
            return { ...old_objects[idx], ...obj_attributes }
        }
    });

    fabric.util.enlivenObjects(new_objects, (objects) => {
        canvas.renderOnAddRemove = false;
        canvas.clear();

        objects.forEach((obj) => {
            canvas.add(obj);
        });
      
        canvas.renderOnAddRemove = true;
        canvas.renderAll();
    });
}