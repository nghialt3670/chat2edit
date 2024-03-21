function toBase64Url(base64Str) {
    return 'data:image/png;base64,' + base64Str
}

function toBase64Str(base64Url) {
    return base64Url.slice(base64Url.indexOf(',') + 1, base64Url.length)
}


function uuidv4() {
    return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}