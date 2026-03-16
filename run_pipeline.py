import subprocess
from email_notifier import send_email


steps = [

    "python news_collector.py",
    "python news_filter.py",
    "python script_generator.py",
    "python voice_generator.py",
    "python subtitle_generator.py",
    "python image_downloader.py",
    "python news_template.py",
    "python shorts_video_generator.py",
    "python youtube_uploader.py"
    send_email(
        "SUCCESS",
        "AI news bot ran successfully and uploaded video."
    )

]

for step in steps:
    print(f"\n🚀 Running: {step}\n")
    subprocess.run(step, shell=True)

print("\n✅ ALL SHORTS UPLOADED SUCCESSFULLY")
