import asyncio
import edge_tts
import os
from datetime import datetime
from ai_voice_gen import generate_ai_audio

timestamp = datetime.now().strftime("%Y-%m-%d")

async def generate_audio():
    os.makedirs("audio", exist_ok=True)

    scripts = [
        f"short1_voice_{timestamp}.txt",
        f"short2_voice_{timestamp}.txt",
        f"short3_voice_{timestamp}.txt",
        f"long_video_voice.txt"
]

    for i, file in enumerate(scripts, start=1):
        with open(f"scripts/{file}", "r", encoding="utf-8") as f:
            text = f.read()

        output_file = f"audio/short{i}_{timestamp}.mp3"

        #Voice: natural female (best for shorts)
        communicate = edge_tts.Communicate(
            text=text,
            voice="en-US-AriaNeural",
            rate="+20%",       # slightly faster (good for reels)
            pitch="+2Hz"
        )

        #voice generate using ai model
        #communicate = generate_ai_audio(text, output_file)

        await communicate.save(output_file)

        print(f"✅ Audio created: {output_file}")

# Run async
asyncio.run(generate_audio())
