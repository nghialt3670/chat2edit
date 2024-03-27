import { v4 as uuidv4 } from 'uuid'


export function toBase64Url(base64Str) {
    return 'data:image/png;base64,' + base64Str
}

export function toBase64Str(base64Url) {
    return base64Url.slice(base64Url.indexOf(',') + 1, base64Url.length)
}

export function objToGraphic(obj) {
    obj = obj.toJSON(['labels', 'uid', 'category']);
    let graphicAttributes = {
        uid: obj.uid,
        labels: obj.labels,
        category: obj.category,
        pos_x: obj.left,
        pos_y: obj.top,
        rotation: obj.angle,
        scale_x: obj.scaleX,
        scale_y: obj.scaleY,
        flip_x: obj.flipX,
        flip_y: obj.flipY,
    }
    if (obj.category == 'base-image') {
        return {
            ...graphicAttributes,
            filters: obj.filters,
            base64: toBase64Str(obj.src),
        }
    } else if (obj.category == 'image-segment') {
        return {
            ...graphicAttributes,
            base64_str: toBase64Str(obj.src),
            score: obj.score,
            inpainted: obj.inpainted,
        }
    }
}

export async function loadFabricImage(url) {
    return new Promise((resolve, reject) => {
        fabric.Image.fromURL(url, (img) => {
            img.set({
                labels: [],
                uid: uuidv4(),
                category: 'base-image',
                selectable: false,
                hoverCursor: "mouse"
            });
            resolve(img);
        }, null, {crossOrigin: 'anonymous'});
    });
}

export async function readFilesToBase64Urls(files) {
    const readFile = (file) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();

            reader.onloadend = () => {
                const base64String = reader.result; 
                resolve(base64String); 
            };

            reader.readAsDataURL(file);
        });
    };

    const filePromises = [];
    for (let i = 0; i < files.length; i++) {
        filePromises.push(readFile(files[i]));
    }

    return Promise.all(filePromises)
        .then((base64Urls) => {
            return base64Urls; 
        })
        .catch((error) => {
            console.error("Error reading files:", error);
        });
}

export async function updateCanvas(canvas, canvasDto) {
    const oldObjects = canvas.getObjects().map(obj => (obj.toJSON()));
    const newObjects = canvasDto.graphics.map(graphic => {
        let attributes = {
            uid: graphic.uuid,
            labels: graphic.labels,
            category: graphic.category,
            left: graphic.pos_x,
            top: graphic.pos_y,
            angle: graphic.rotation,
            scaleX: graphic.scale_x,
            scaleY: graphic.scale_y,
            flipX: graphic.flip_x,
            flipY: graphic.flip_y,
        }
        if (graphic.category === 'base-image') {
            attributes = {
                ...attributes, 
                src: toBase64Url(graphic.base64),
                filters: graphic.filters,
                selectable: false,
                hoverCursor: "mouse"
            }
        } else if (graphic.category === 'image-segment') {
            attributes = {
                ...attributes,
                src: toBase64Url(graphic.base64),
                filters: graphic.filters,
                score: graphic.score,
                inpainted: graphic.inpainted,
            }
        } else if (graphic.category === 'text') {
            throw Error('implement text');
        }

        const idx = oldObjects.findIndex(obj => (obj.uid === graphic.uid));

        if (idx != -1) {
            return { ...oldObjects[idx], ...attributes, };
        } else {
            const image = new fabric.Image('');
            return { ...image.toJSON(), ...attributes };          
        }
    });

    return new Promise((resolve, reject) => {
        fabric.util.enlivenObjects(newObjects, objects => {
            console.log(objects);
            canvas.renderOnAddRemove = false;
            canvas.clear();
    
            objects.forEach((obj, i) => {
                canvas.insertAt(obj, i);
            });
    
            canvas.renderOnAddRemove = true;
            canvas.renderAll();
            resolve(canvas);
        });
    });
    
}