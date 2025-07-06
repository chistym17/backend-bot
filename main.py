from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pipeline_setup import create_pipeline
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/audio")
async def audio_websocket(websocket: WebSocket):
    await websocket.accept()
    pipeline = await create_pipeline()

    try:
        while True:
            data = await websocket.receive_bytes()
            response = await pipeline.push_audio(data)
            if response:
                await websocket.send_bytes(response)
    except WebSocketDisconnect:
        await pipeline.close()
        print("Client disconnected")
