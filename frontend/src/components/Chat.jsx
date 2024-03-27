import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fabric } from 'fabric';
import { v4 as uuidv4 } from 'uuid'
import Message from './Message.jsx';
import { 
    toBase64Str, 
    toBase64Url, 
    objToGraphic, 
    loadFabricImage, 
    readFilesToBase64Urls,
    updateCanvas
}  from './helpers.js';
import ChatForm from './ChatForm.jsx';


function Chat() {
    const navigate = useNavigate();
    const [messages, setMessages] = useState([]); 
    const maxHeight = 500;

    const handleNavigateClick = (e) => {
        navigate('/edit')
    }

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
            canvas.add(img);
            canvases.push(canvas);
        }
        
        const message = {
            key: uuidv4(),
            side: 'right', 
            canvases: canvases, 
            text: textInput
        };
        
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
        return
    
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

    const toMessageComponent = (msg) => {
        return (
            <Message
                {...msg}
                handleNavigateClick={handleNavigateClick}
            />
        )
    }
 
    return (
        <>
            <div id='chat-box'>
                <div id='msg-area'>
                    {messages.map(toMessageComponent)}
                </div>
                <ChatForm handleSendMessage={handleSendMessage}/>
            </div>
        </>
    );
}

export default Chat;
