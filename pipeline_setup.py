from pipecat.pipeline import pipeline
from pipecat.services.google.llm import GoogleLLMService
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from tools import FormFillingTool
import os

async def create_pipeline():
    llm = GoogleLLMService(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini-2.0-flash",
        system_instruction="You are a helpful assistant with access to current information.",
        tools=[FormFillingTool()],
        params=GoogleLLMService.InputParams(
            temperature=0.7,
            max_tokens=1000
        )
    )

    pipeline = pipeline([llm])
    await pipeline.initialize()
    return pipeline 