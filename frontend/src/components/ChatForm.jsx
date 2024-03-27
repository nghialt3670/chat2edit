import React, { useState } from 'react';
import { readFilesToBase64Urls } from './helpers';



export default function ChatForm({ handleFileChange, handleSendMessage }) {
    const [base64Urls, setBase64Urls] = useState([]);
    const [textInput, setTextInput] = useState('');

    const handleFileChange = async (e) => {
        e.preventDefault();
        const files = e.target.files;
        const loadedBase64Urls = await readFilesToBase64Urls(files);
        setBase64Urls(loadedBase64Urls);
    };

    const handleUploadClick = (e) => {
        e.preventDefault();
        document.getElementById('img-input').click();
    };

    const deleteImage = (idx) => {
        document.getElementById('img-input').value='';
        setBase64Urls(base64Urls.slice(0, idx).concat(base64Urls.slice(idx + 1, base64Urls.length)));
    }

    return (
        <form id='chat-form' >
            <div id='img-preview-area'>
                {base64Urls.map((url, idx) => (
                    <div key={idx} className='img-preview'>
                        <img 
                            src={url} 
                            alt="" 
                        />
                        <input 
                            type='button' 
                            className='del-img-btn' 
                            onClick={(e) => deleteImage(idx)}
                        />
                    </div>
                ))}
            </div>
            <div id='input-area'>
                <input 
                    type='file' 
                    name='' 
                    id='img-input' 
                    style={{ display: 'none' }} 
                    accept="image/*" 
                    multiple 
                    onChange={handleFileChange} 
                />

                <input 
                    type='button'
                    id='upload-img-btn'
                    onClick={handleUploadClick}
                />

                <input 
                    type='text' 
                    id='ins-input'
                    onChange={(e) => setTextInput(e.target.value)}
                    value={textInput} />

                <input
                    type='button' 
                    id='send-msg-btn'
                    onClick={handleSendMessage} 
                />
            </div>
            
        </form>
    )
}
