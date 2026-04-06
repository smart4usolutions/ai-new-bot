import subprocess
import os
import time
import sys

os.makedirs("audio", exist_ok=True)
os.makedirs("videos", exist_ok=True)
os.makedirs("data", exist_ok=True)

steps = [
    "python news_collector.py",
    "python news_filter.py",
    "python image_downloader.py",
    "python news_template.py",
    "python script_generator.py",
    #"python voice_generator.py",
    # "python subtitle_generator.py",
    #"python shorts_video_generator.py",
    #"python youtube_uploader.py"
]

MAX_RETRIES = 3  # total attempts

for step in steps:
    print(f"\n🚀 Running: {step}\n")

    success = False

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"🔁 Attempt {attempt} for {step}")

        result = subprocess.run(step, shell=True)

        if result.returncode == 0:
            print(f"✅ Success: {step}")
            success = True
            break
        else:
            print(f"❌ Failed attempt {attempt}: {step}")
            time.sleep(3)  # small delay before retry

    if not success:
        print(f"\n💥 CRITICAL FAILURE: {step} failed after {MAX_RETRIES} attempts")
        print("⛔ Stopping pipeline...\n")

        # OPTIONAL: send failure email here
        # send_email("FAILED", f"{step} failed after retries")

        sys.exit(1)  # 🚨 STOP EVERYTHING

print("\n🎉 Pipeline Run Successful!!!")
