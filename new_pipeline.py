from pipecat.services.gemini_multimodal_live.gemini import GeminiMultimodalLiveLLMService
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.task import PipelineTask
from pipecat.transports.services.daily import DailyTransport, DailyParams
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.processors.frameworks.rtvi import RTVIProcessor, RTVIObserver, RTVIConfig
from pipecat.pipeline.runner import PipelineRunner
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

async def start_pipeline():
    llm = GeminiMultimodalLiveLLMService(
        api_key=os.getenv("GEMINI_API_KEY"),
        voice_id="Puck",
        transcribe_user_audio=True,
        enable_tool_calling=True
    )

    context = OpenAILLMContext([
        {
            "role": "user",
            "content": "You are a friendly assistant that speaks clearly and helps users fill out forms via voice.",
        }
    ])
    context_aggregator = llm.create_context_aggregator(context)


    transport = DailyTransport(
        room_url="https://chisty.daily.co/Vf8IldEOuTmG7zzVGHFd",
        token=os.getenv("DAILY_TOKEN"),
        bot_name="VoiceBot",
        params=DailyParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            video_out_enabled=False,
            vad_analyzer=SileroVADAnalyzer()
        )
    )

    rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

    pipeline = Pipeline([
        transport.input(),
        rtvi,
        context_aggregator.user(),
        llm,
        transport.output(),
        context_aggregator.assistant(),
    ])

    task = PipelineTask(pipeline, observers=[RTVIObserver(rtvi)])

    runner = PipelineRunner()
    await runner.run(task)

async def main():
    print("Starting Gemini Multimodal Live Pipeline...")
    try:
        await start_pipeline()
    except Exception as e:
        print(f"Error running pipeline: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
