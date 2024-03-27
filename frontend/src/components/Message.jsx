import React from 'react';
import { ImageList, ImageListItem } from '@mui/material';

function ImageContainer ({ canvases, handleNavigateClick }) {
    if (canvases.length == 0) return undefined;
    return (
        <ImageList
            variant="masonry" 
            cols={Math.ceil(Math.sqrt(canvases.length))} 
            gap={10}
            sx={{ margin: 0 }}
            className='msg-img-containter'
        >
            {canvases.map((canvas) => (
                <ImageListItem key={canvas.uid}>
                    <div className='msg-img'>
                        <img
                            src={canvas.toDataURL()}
                        />
                        <input 
                            type='button'
                            className='nav-to-edit-btn'
                            onClick={handleNavigateClick}
                        />
                    </div>
                </ImageListItem>
            ))}
        </ImageList>
    )
}


export default function Message({ side, canvases, text, handleNavigateClick }) {
    return (
        <div className={`msg ${side}-msg`} >
            <div className='msg-content'>
                <ImageContainer
                    canvases={canvases}
                    handleNavigateClick={handleNavigateClick}
                /> 
                <p>{text}</p>
            </div> 
        </div>
    )
}
