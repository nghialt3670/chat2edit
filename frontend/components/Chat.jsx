import React, { useState, useEffect } from 'react';


class Message {
	constructor(position, base64Urls=undefined, text=undefined) {
        this.position = position
		this.base64Urls = base64Urls 
		this.text = text;
	}
}


function Chat() {
    const [messages, setMessages] = useState([]); 
    const [base64Urls, setBase64Urls] = useState([]);
    const [textInput, setTextInput] = useState('');

    const handleFileChange = (event) => {
        const files = event.target.files;

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

        Promise.all(filePromises)
            .then((base64Results) => {
                setBase64Urls(base64Results); 
            })
            .catch((error) => {
                console.error("Error reading files:", error);
            });
    };

    const handleUploadClick = () => {
        document.getElementById('img-input').click();
    };

    const handleSendMessage = () => {
        const message = new Message('right', base64Urls, textInput);
        setBase64Urls([]);
        setTextInput('');
        setMessages((prev) => [message, ...prev]);
        
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
                                {msg.base64Urls ? 
                                    msg.base64Urls.map((url, idx) => (
                                        <img 
                                            key={idx}
                                            src={url} 
                                            alt="" 
                                        />
                                    )) 
                                    : undefined
                                }
                                <p>{msg.text}</p>
                            </div> 

                        </div>
                    ))}
                </div>
                <form action='' method='post' id='chat-form' >
                    <div id='img-preview'>
                        {base64Urls.map((base64Str, idx) => (
                            <img 
                                key={idx}
                                src={base64Str} 
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
