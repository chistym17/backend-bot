from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pipeline_setup import create_pipeline
from pipecat.frames.frames import AudioRawFrame
from pipecat.pipeline.runner import PipelineRunner
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
    
    # Create pipeline task and context aggregator
    task, context_aggregator = await create_pipeline()
    
    # Create pipeline runner
    runner = PipelineRunner()
    
    try:
        # Queue initial context frame
        await task.queue_frames([context_aggregator.user().get_context_frame()])
        
        # Start the pipeline
        await runner.run(task)
        
        while True:
            data = await websocket.receive_bytes()
            
            # Create audio frame and queue it
            audio_frame = AudioRawFrame(
                audio=data,
                sample_rate=16000,
                num_channels=1
            )
            await task.queue_frames([audio_frame])
            
    except WebSocketDisconnect:
        await runner.stop()
        print("Client disconnected")
