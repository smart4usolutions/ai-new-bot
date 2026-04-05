import asyncio
import os
from datetime import datetime
from ai_voice_gen import generate_ai_audio

timestamp = datetime.now().strftime("%Y-%m-%d")

async def generate_audio():
    os.makedirs("audio", exist_ok=True)

    scripts = [
        f"short1_voice_{timestamp}.txt",
        f"short2_voice_{timestamp}.txt",
        f"short3_voice_{timestamp}.txt"
]

    for i, file in enumerate(scripts, start=1):
        with open(f"scripts/{file}", "r", encoding="utf-8") as f:
            text = f.read()

        output_file = f"audio/short{i}_{timestamp}.mp3"

        #voice generate using ai model
        success = generate_ai_audio(text, output_file)

        if not success:
            print(f"❌ Failed to generate audio for {file}")
            continue

        print(f"✅ Audio created: {output_file}")

# Run async
asyncio.run(generate_audio())
