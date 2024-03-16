const canvas = new fabric.Canvas('canvas');
const uploadedImage = document.getElementById('uploadedImage');
const addedImage = document.getElementById('addedImage');
const uploadBtn = document.getElementById('uploadBtn');
const addBtn = document.getElementById('addBtn')
const canvasSize = document.getElementById('canvasSize');
const containerHeight = 600;
const containerWidth = 1000;
const maxHeight = 600;
const maxWidth = 1000;

const scaleRatio = Math.min(containerWidth/maxWidth, containerHeight/maxHeight);
canvas.setDimensions({ width: canvas.getWidth() * scaleRatio, height: canvas.getHeight() * scaleRatio });
canvas.setZoom(scaleRatio)

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
                    labels: [],
                    uuid: uuidv4(),
                    category: 'base-image',
                    selectable: false,
                    hoverCursor: "mouse",
                });
                canvas.setWidth(maxHeight * (img.width / img.height));
                canvas.set({
                    fitWith: canvas.width,
                    fitHeight: canvas.height
                })
                canvas.setZoom(canvas.height/img.height)
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
                    labels: [],
                    uuid: uuidv4(),
                    category: 'base-image',
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


