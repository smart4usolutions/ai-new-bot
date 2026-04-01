import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# Load filtered news
with open("data/filtered_news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

news_text = ""

for i, item in enumerate(news):
    title = item.get("title", "")
    desc = item.get("description", "")
    news_text += f"{i+1}. {title} - {desc}\n"


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
 ],

 "long_video":[
  {{"headline":"", "narration":""}},
  {{"headline":"", "narration":""}},
  {{"headline":"", "narration":""}},
  {{"headline":"", "narration":""}},
  {{"headline":"", "narration":""}},
  {{"headline":"", "narration":""}},
  {{"headline":"", "narration":""}},
  {{"headline":"", "narration":""}},
  {{"headline":"", "narration":""}},
  {{"headline":"", "narration":""}}
 ]
}}

Rules:

Shorts narration = about 40-50 words each  
Long video narration = about 60 words each  
Narration should NOT include instructions like Hook or Scene.
Add this line at last = follow for daily ai updates.
Larration should start with catchy hook as it is youtube shorts

News:

{news_text}
"""

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "qwen/qwen3.6-plus-preview:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
)

result = response.json()

if "choices" in result:
    content = result["choices"][0]["message"]["content"]
    content = content.strip().replace("```json", "").replace("```", "")
    print("\nRAW RESPONSE FROM MODEL:\n")
    print(content)
else:
    print("❌ API Error:", result)
    content = None

print("\nRAW RESPONSE FROM MODEL:\n")
# print(content)

# Clean markdown
content = content.strip().replace("```json", "").replace("```", "")

try:
    scripts = json.loads(content)

except json.JSONDecodeError:
    print("❌ JSON parsing failed")

    os.makedirs("scripts", exist_ok=True)

    with open("scripts/debug_response.txt", "w", encoding="utf-8") as f:
        f.write(content)

    print("Raw response saved to scripts/debug_response.txt")
    exit()


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

    with open(f"scripts/short{i}_voice.txt", "w", encoding="utf-8") as f:
        f.write(narration_text.strip())


# Save long video narration
long_text = ""

for news in scripts["long_video"]:
    long_text += news["narration"] + " "

with open("scripts/long_video_voice.txt", "w", encoding="utf-8") as f:
    f.write(long_text.strip())


print("\n✅ Scripts generated and saved successfully")
