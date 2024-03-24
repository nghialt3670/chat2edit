import React, { useState, useEffect } from 'react';
import { fabric } from 'fabric';
import { 
    uuidv4, 
    toBase64Str, 
    toBase64Url, 
    objToGraphic, 
    loadFabricImage, 
    readFilesToBase64Urls,
    updateCanvas
}  from './helpers.js';


class Message {
	constructor(position, canvases=undefined, text=undefined) {
        this.position = position
		this.canvases = canvases 
		this.text = text;
	}
}


function Chat() {
    const [messages, setMessages] = useState([]); 
    const [base64Urls, setBase64Urls] = useState([]);
    const [textInput, setTextInput] = useState('');
    const maxHeight = 500;

    const handleFileChange = async (event) => {
        const files = event.target.files;
        const loadedBase64Urls = await readFilesToBase64Urls(files);
        setBase64Urls(loadedBase64Urls);
    };

    const handleUploadClick = () => {
        document.getElementById('img-input').click();
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        document.getElementById('img-input').value = '';

        const canvases = [];
        for (const url of base64Urls) {
            const canvas = new fabric.Canvas();
            canvas.set({uid: uuidv4()})
            const img = await loadFabricImage(url);
            canvas.setHeight(maxHeight)
            canvas.setWidth(maxHeight * (img.width / img.height));
            canvas.setZoom(canvas.height / img.height);
            canvas.clear();
            canvas.add(img);
            canvases.push(canvas);
        }
        
        const message = new Message('right', canvases, textInput);
        
        setBase64Urls([]);
        setTextInput('');
        setMessages((prev) => [message, ...prev]);

        const canvases_data = canvases.map((canvas) => ({
            uid: canvas.uid,
            graphics: canvas.getObjects().map(objToGraphic)
        }));

        const requestBody = JSON.stringify(canvases_data);
    
        const request = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: requestBody,
        }
    
        const endpoint = 'http://127.0.0.1:8000/edit';
        const param = new URLSearchParams({instruction: textInput})
        const parameterized_endpoint = endpoint + '?' + param
        const response = await fetch(parameterized_endpoint, request);
        const data = await response.json();
        const newCanvasesDto = data['canvases'];
        const newCanvases = []
        for (let i = 0; i < canvases.length; i++) {
            const cloneCanvas = async canvas => (
                new Promise((resolve, reject) => {
                    canvas.clone(canvas => { resolve(canvas); });
                })
            );
            const clonedCanvas = await cloneCanvas(canvases[i]);
            const updatedCanvas = await updateCanvas(clonedCanvas, newCanvasesDto[i]);
            const base_image = updatedCanvas.getObjects()[0];

            updatedCanvas.setHeight(maxHeight)
            updatedCanvas.setWidth(maxHeight * (base_image.width / base_image.height));
            updatedCanvas.setZoom(updatedCanvas.height / base_image.height);
            newCanvases.push(updatedCanvas);
        }
        const responseMessage = new Message('left', newCanvases);
        setMessages((prev) => [responseMessage, ...prev]);
    }
 
    return (
        <>
            <div id='chat-box'>
                <div id='msg-area'>
                    {messages.map((msg, idx) => (
                        <div 
                            id={idx} 
                            key={idx}
                            className={`msg ${msg.position}-msg`} >

                            <div className='msg-content'>
                                {msg.canvases ? 
                                    msg.canvases.map((canvas, idx) => (
                                        <img 
                                            key={idx}
                                            src={canvas.toDataURL()} 
                                            alt="hihi" 
                                        />
                                    )) 
                                    : undefined
                                }
                                <p>{msg.text}</p>
                            </div> 

                        </div>
                    ))}
                </div>
                <form action='' method='post' id='chat-form' onSubmit={handleSendMessage} >
                    <div id='img-preview'>
                        {base64Urls.map((url, idx) => (
                            <img 
                                key={idx}
                                src={url} 
                                alt="" 
                            />
                        ))}
                    </div>
                    <div id='input-area'>
                        <input 
                            type='file' 
                            name='' 
                            id='img-input' 
                            style={{ display: 'none' }} 
                            accept="image/*" 
                            multiple onChange={handleFileChange} />

                        <input 
                            type="button" 
                            value="+" 
                            id='upload-img-btn' 
                            onClick={handleUploadClick} />

                        <input 
                            type='text' 
                            id='ins-input'
                            onChange={(e) => setTextInput(e.target.value)}
                            value={textInput} />

                        <input 
                            type='button' 
                            value='Send' 
                            id='send-msg-btn'
                            onClick={handleSendMessage} />
                    </div>
                    
                </form>
            </div>
        </>
    );
}

export default Chat;
