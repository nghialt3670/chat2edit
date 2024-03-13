const canvas = new fabric.Canvas('canvas');
const uploadedImage = document.getElementById('uploadedImage');
const addedImage = document.getElementById('addedImage');
const uploadBtn = document.getElementById('uploadBtn');
const addBtn = document.getElementById('addBtn')
const canvasSize = document.getElementById('canvasSize');
const maxHeight = 600;
const maxWidth = 1000;
canvas.setHeight(maxHeight);
canvas.setWidth(maxWidth);
canvas.set({
    fitWith: maxWidth,
    fitHeight: maxHeight
})


uploadBtn.onclick = (e) => {
    uploadedImage.click();
} 

addBtn.onclick = (e) => {
    addedImage.click();
}


canvasSize.onchange = (e) => {
    const selectedOption = canvasSize.value;
    if (selectedOption === 'fit') {
        canvas.setWidth(canvas.fitWith);
        canvas.setHeight(canvas.fitHeight);
    } else {
        const ratioParts = selectedOption.split(':');
        const ratioWidth = parseInt(ratioParts[0]);
        const ratioHeight = parseInt(ratioParts[1]);
        width = ratioWidth / ratioHeight * maxHeight;
        canvas.setWidth(width);
    }
}


uploadedImage.onchange =  async (e) => {
    const file = e.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            fabric.Image.fromURL(e.target.result, async (img) => {
                const scale = maxHeight / img.height;
                img.set({
                    uuid: uuidv4(),
                    category: 'target-image',
                    selectable: false,
                    scaleX: scale,
                    scaleY: scale,
                    hoverCursor: "mouse",
                    members: []
                });
                canvas.setWidth(maxHeight * (img.width / img.height));
                canvas.set({
                    fitWith: canvas.width,
                    fitHeight: canvas.height
                })
                canvas.clear();
                canvas.add(img);
            });
        };
        reader.readAsDataURL(file);
    }
};


addedImage.onchange =  async (e) => {
    const file = e.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            fabric.Image.fromURL(e.target.result, async (img) => {
                const scale = maxHeight / img.height * 0.7;

                img.set({
                    uuid: uuidv4(),
                    category: 'basic-image',
                    scaleX: scale,
                    scaleY: scale,
                });
                canvas.add(img);
            });
        };
        reader.readAsDataURL(file);
    }
};


function deleteActiveObject() {
    var activeObject = canvas.getActiveObject();
    if (activeObject) {
        canvas.remove(activeObject);
        canvas.renderAll();
    }
}

window.onkeydown = (e) => {
    if (e.key === 'Delete' || e.key === 'Backspace') {
        deleteActiveObject();
    }
}





function uuidv4() {
    return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}