import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

# Load env variables
load_dotenv()

api_key = os.getenv("ELEVEN_API_KEY")

if not api_key:
    raise ValueError("❌ ELEVEN_API_KEY not found")

client = ElevenLabs(api_key=api_key)

# Ensure folder exists
os.makedirs("audio", exist_ok=True)

# Read scripts
scripts = [f for f in os.listdir("scripts") if f.endswith(".txt")]

if not scripts:
    print("❌ No scripts found")
    exit(1)

for i, file in enumerate(scripts, start=1):
    with open(f"scripts/{file}", "r", encoding="utf-8") as f:
        text = f.read()

    print(f"🎤 Generating audio for: {file}")

    try:
        audio = client.text_to_speech.convert(
            text=text,
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel voice
            model_id="eleven_turbo_v2"
        )

        output_file = f"audio/short{i}.mp3"

        with open(output_file, "wb") as out:
            for chunk in audio:
                out.write(chunk)

        print(f"✅ Audio created: {output_file}")

    except Exception as e:
        print(f"❌ Failed: {file}")
        print(str(e))
        exit(1)
