import asyncio
import edge_tts
import os

async def generate_audio():
    os.makedirs("audio", exist_ok=True)

    scripts = sorted([f for f in os.listdir("scripts") if f.endswith(".txt")])

    for i, file in enumerate(scripts, start=1):
        with open(f"scripts/{file}", "r", encoding="utf-8") as f:
            text = f.read()

        output_file = f"audio/short{i}.mp3"

        # Voice: natural female (best for shorts)
        communicate = edge_tts.Communicate(
            text=text,
            voice="en-US-AriaNeural",
            rate="+5%",       # slightly faster (good for reels)
            pitch="+2Hz"
        )

        await communicate.save(output_file)

        print(f"✅ Audio created: {output_file}")

# Run async
asyncio.run(generate_audio())
