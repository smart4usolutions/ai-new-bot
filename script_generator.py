import json
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Setup
timestamp = datetime.now().strftime("%Y-%m-%d")
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print("OPENROUTER API KEY PRESENT:", bool(OPENROUTER_API_KEY))

if not OPENROUTER_API_KEY:
    print("❌ ERROR: OPENROUTER_API_KEY missing")
    exit(1)

# Load filtered news
with open("data/filtered_news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

news_text = ""
for i, item in enumerate(news):
    title = item.get("title", "")
    desc = item.get("description", "")
    news_text += f"{i+1}. {title} - {desc}\n"

# Prompt
prompt = f"""
You are a viral YouTube Shorts script writer for a US audience.

Return ONLY VALID JSON.

{{
 "shorts":[
  [
   {{"headline":"", "narration":""}},
   {{"headline":"", "narration":""}},
   {{"headline":"", "narration":""}}
  ],
  [
   {{"headline":"", "narration":""}},
   {{"headline":"", "narration":""}},
   {{"headline":"", "narration":""}}
  ],
  [
   {{"headline":"", "narration":""}},
   {{"headline":"", "narration":""}},
   {{"headline":"", "narration":""}}
  ]
 ]
}}

Rules:
- 40–55 words each
- conversational tone
- every 3rd narration ends with: Follow for daily global updates.

News:
{news_text}
"""

def clean_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
    text = text.replace("json\n", "").replace("json", "")
    start = text.find("{")
    end = text.rfind("}") + 1
    return text[start:end]

def call_openrouter_with_fallback(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    models = [
        "z-ai/glm-4.5-air:free",
        "arcee-ai/trinity-large-preview:free",
        "google/gemma-4-26b-a4b-it:free"
    ]

    for model in models:
        try:
            print(f"🚀 Trying: {model}")

            response = requests.post(
                url,
                headers=headers,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"},
                },
                timeout=25
            )

            result = response.json()
            content = result["choices"][0]["message"]["content"]
            content = clean_json(content)

            return json.loads(content)

        except Exception as e:
            print("❌ Failed:", model, e)

    return None

# Generate scripts
scripts = call_openrouter_with_fallback(prompt)

if not scripts:
    print("❌ All models failed")
    exit()

print("✔️ JSON parsing Done")

# Ensure folder
os.makedirs("scripts", exist_ok=True)

# Save full JSON
with open("scripts/video_scripts.json", "w", encoding="utf-8") as f:
    json.dump(scripts, f, indent=2)

# 🔥 NEW LOGIC (9 FILES)
for short_index, short in enumerate(scripts["shorts"], start=1):
    
    for voice_index, news_item in enumerate(short, start=1):

        narration = news_item["narration"]

        filename = f"short{short_index}_voice{voice_index}_{timestamp}.txt"

        with open(f"scripts/{filename}", "w", encoding="utf-8") as f:
            f.write(narration.strip())

        print("Saved:", filename)

print("\n✅ 9 Scripts generated successfully")
