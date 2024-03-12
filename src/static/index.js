var canvas = new fabric.Canvas('canvas');
canvas.setHeight(600); 
canvas.setWidth(800);


const uploadImage = document.getElementById('uploadImage');
const uploadBtn = document.getElementById('uploadBtn');
const editBtn = document.getElementById('editBtn');


uploadBtn.onclick = (e) => {
    uploadImage.click();
} 


uploadImage.onchange =  async (e) => {
    const file = e.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            fabric.Image.fromURL(e.target.result, async (img) => {
                const scaleFactor = canvas.height / img.height;
                img.set({
                    uuid: uuidv4(),
                    category: 'basic-image',
                    scaleX: scaleFactor,
                    scaleY: scaleFactor,
                    selectable: false,
                    hoverCursor: "mouse"
                });

                canvas.setWidth(img.width * scaleFactor); 
                canvas.clear();
                canvas.add(img);
            });
        };
        reader.readAsDataURL(file);
    }
};


editBtn.onclick = async (e) => {
    const instruction = document.getElementById('instruction');
    const endpoint = '/edit';

    if (instruction.value.trim() == '') {
        alert('Please give your instruction to edit the image')
        return
    }

    objects = canvas.getObjects().map(
        obj => obj.toJSON(['uuid', 'category'])
    );

    requestBody = JSON.stringify({
        'objects': objects,
        'instruction': instruction.value 
    });

    request = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: requestBody,
    }

    const response = await fetch(endpoint, request);
    const new_objects = await response.json()

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


function uuidv4() {
    return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}