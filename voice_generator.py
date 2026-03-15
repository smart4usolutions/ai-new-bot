import os
import subprocess

# Piper settings
PIPER_PATH = r"C:\Users\Dell\OneDrive\Desktop\ai_news_automation\piper\piper.exe"
VOICE_MODEL = r"C:\Users\Dell\OneDrive\Desktop\ai_news_automation\piper\en_US-lessac-medium.onnx"

scripts_folder = "scripts"
audio_folder = "audio"

os.makedirs(audio_folder, exist_ok=True)

files = [
    "short1_voice.txt",
    "short2_voice.txt",
    "short3_voice.txt",
    "long_video_voice.txt"
]

for file in files:
    
    input_path = os.path.join(scripts_folder, file)

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    output_audio = file.replace("_voice.txt", ".wav")
    output_path = os.path.join(audio_folder, output_audio)

    command = [
        PIPER_PATH,
        "-m", VOICE_MODEL,
        "-f", output_path
    ]

    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    process.communicate(input=text.encode("utf-8"))

    print(f"✅ Generated audio: {output_audio}")

print("\n🎙️ All voice files generated successfully!")
