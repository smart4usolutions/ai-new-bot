import os
from elevenlabs import generate, save, set_api_key

set_api_key(os.getenv("ELEVEN_API_KEY"))

os.makedirs("audio", exist_ok=True)

scripts = [f for f in os.listdir("scripts") if f.endswith(".txt")]

for i, file in enumerate(scripts, start=1):
    with open(f"scripts/{file}", "r", encoding="utf-8") as f:
        text = f.read()

    audio = generate(
        text=text,
        voice="Rachel",
        model="eleven_monolingual_v1"
    )

    output_file = f"audio/short{i}.mp3"
    save(audio, output_file)

    print(f"✅ Audio created: {output_file}")
