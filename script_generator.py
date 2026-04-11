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
You are a YouTube news script writer.

Based on the following AI news create scripts.

Return ONLY VALID JSON. No explanations.

Structure:

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
Shorts narration = about 40-50 words each  
Narration should NOT include instructions like Hook or Scene.
Add this line at last of every 3rd narration = follow for daily global updates.
Narration should start with catchy hook as it is youtube shorts
Make it engaging, fast-paced, and conversational.
Avoid robotic tone.

News:
{news_text}
"""

# Clean JSON function
def clean_json(text):
    text = text.strip()

    if text.startswith("```"):
        text = text.split("```")[1]

    text = text.replace("json\n", "").replace("json", "")

    start = text.find("{")
    end = text.rfind("}") + 1

    return text[start:end]

# 🔥 Fallback API Call Function
def call_openrouter_with_fallback(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/smart4usolutions",
        "X-Title": "AI News Bot"
    }

    models_to_try = [
        "stepfun/step-3.5-flash:free",   #primary model
        "google/gemma-4-26b-a4b-it:free",   #fallback model
        "nvidia/nemotron-3-super-120b-a12b:free",    #fallback model
        "arcee-ai/trinity-large-preview:free",
        "z-ai/glm-4.5-air:free"
    ]

    for model in models_to_try:
        try:
            print(f"\n🚀 Trying model: {model}")

            response = requests.post(
                url=url,
                headers=headers,
                json={
                    "model": model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "response_format": {"type": "json_object"},
                },
                timeout=25
            )

            response.raise_for_status()
            result = response.json()

            if "choices" not in result:
                print(f"❌ Invalid response from {model}")
                continue

            content = result["choices"][0]["message"]["content"]
            content = content.strip().replace("```json", "").replace("```", "")

            content = clean_json(content)

            # Validate JSON
            scripts = json.loads(content)

            print(f"✅ Success with model: {model}")
            return scripts, content

        except Exception as e:
            print(f"❌ Model failed: {model}")
            print("Error:", e)

    return None, None

# 🚀 Call with fallback
scripts, raw_content = call_openrouter_with_fallback(prompt)

if not scripts:
    print("❌ All models failed")

    os.makedirs("scripts", exist_ok=True)
    with open("scripts/debug_response.txt", "w", encoding="utf-8") as f:
        if raw_content:
            f.write(raw_content)

    exit()

print("✔️ JSON parsing Done")

# Ensure scripts folder exists
os.makedirs("scripts", exist_ok=True)

# Save full JSON
with open("scripts/video_scripts.json", "w", encoding="utf-8") as f:
    json.dump(scripts, f, indent=2)

# Save shorts narration
for i, short in enumerate(scripts["shorts"], start=1):
    narration_text = ""

    for news in short:
        narration_text += news["narration"] + " "

    with open(f"scripts/short{i}_voice_{timestamp}.txt", "w", encoding="utf-8") as f:
        f.write(narration_text.strip())

print("\n✅ Scripts generated and saved successfully")