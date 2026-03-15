import os
import re

script_folder = "scripts"
output_folder = "subtitles"

os.makedirs(output_folder, exist_ok=True)

def seconds_to_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

for i in range(1,4):

    with open(f"{script_folder}/short{i}_voice.txt","r",encoding="utf-8") as f:
        text = f.read()

    words = re.findall(r'\w+', text)

    word_duration = 0.45   # average speaking speed
    chunk_size = 4         # words per subtitle

    subtitles = []
    start = 0

    for j in range(0,len(words),chunk_size):

        chunk = words[j:j+chunk_size]
        duration = len(chunk) * word_duration
        end = start + duration

        subtitles.append({
            "start": start,
            "end": end,
            "text": " ".join(chunk)
        })

        start = end

    srt_path = f"{output_folder}/short{i}.srt"

    with open(srt_path,"w",encoding="utf-8") as f:

        for idx,sub in enumerate(subtitles,1):

            f.write(f"{idx}\n")
            f.write(f"{seconds_to_timestamp(sub['start'])} --> {seconds_to_timestamp(sub['end'])}\n")
            f.write(f"{sub['text']}\n\n")

    print(f"✅ subtitles created: {srt_path}")
