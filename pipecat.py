from pipecat import Pipeline
from pipecat_gemini import GeminiLiveNode
from tools import FormFillingTool
import os

async def create_pipeline():
    gemini_node = GeminiLiveNode(
        api_key=os.getenv("GEMINI_API_KEY"),
        tools=[FormFillingTool()],
        interruptible=True,
        voice_output=True,
    )

    pipeline = Pipeline()
    pipeline.add_node(gemini_node)

    await pipeline.initialize()
    return pipeline
