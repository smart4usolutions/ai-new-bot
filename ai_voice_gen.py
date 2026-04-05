import requests
import time
import os

WAVESPEED_API_KEY = os.getenv("WAVESPEED_API_KEY")

def generate_ai_audio(script_text, output_file):

    submit_url = "https://api.wavespeed.ai/api/v3/wavespeed-ai/qwen3-tts/text-to-speech"

    headers = {
        "Authorization": f"Bearer {WAVESPEED_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": script_text,
        "language": "English",
        "voice": "Dylan",  # try: Dylan, Eric, etc.
        "style_instruction": "Energetic breaking news reporter, fast-paced, engaging and dramatic"
    }

    try:
        # STEP 1: Submit job
        response = requests.post(submit_url, headers=headers, json=payload)

        if response.status_code != 200:
            print("❌ Submit Error:", response.text)
            return False

        task_id = response.json()["data"]["id"]
        print("🟡 Task ID:", task_id)

        # STEP 2: Poll result
        result_url = f"https://api.wavespeed.ai/api/v3/predictions/{task_id}/result"

        for _ in range(30):  # wait max ~30 sec
            time.sleep(5)

            result = requests.get(result_url, headers=headers)
            data = result.json()

            if data.get("data", {}).get("outputs"):
                audio_url = data["data"]["outputs"][0]
                print("✅ Audio URL:", audio_url)

                # STEP 3: Download file
                audio_data = requests.get(audio_url).content

                with open(output_file, "wb") as f:
                    f.write(audio_data)

                print("✅ Saved:", output_file)
                return True

            print("⏳ Waiting for audio...")

        print("❌ Timeout: Audio not ready")
        return False

    except Exception as e:
        print("❌ Exception:", e)
        return False
