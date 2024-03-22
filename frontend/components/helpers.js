export function toBase64Url(base64Str) {
    return 'data:image/png;base64,' + base64Str
}

export function toBase64Str(base64Url) {
    return base64Url.slice(base64Url.indexOf(',') + 1, base64Url.length)
}

export function uuidv4() {
    return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

export function objToGraphic(obj) {
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
}

export async function loadFabricImage(url) {
    return new Promise((resolve, reject) => {
        fabric.Image.fromURL(url, (img) => {
            img.set({
                labels: [],
                uuid: uuidv4(),
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