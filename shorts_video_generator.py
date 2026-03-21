import os
import subprocess

audio_folder = "audio"
image_folder = "formatted_images"
output_folder = "videos"

os.makedirs(output_folder, exist_ok=True)

def get_audio_duration(audio_file):

    result = subprocess.run(
        [
            #"bin/ffprobe.exe",
            "ffprobe",
            "-v","error",
            "-show_entries","format=duration",
            "-of","default=noprint_wrappers=1:nokey=1",
            audio_file
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    return float(result.stdout)

for i in range(1,4):

    audio_file = f"{audio_folder}/short{i}.mp3"
    music_file = "music/news_music.mp3"

    img1 = f"{image_folder}/news{(i-1)*3+1}.jpg"
    img2 = f"{image_folder}/news{(i-1)*3+2}.jpg"
    img3 = f"{image_folder}/news{(i-1)*3+3}.jpg"

    output_file = f"{output_folder}/short{i}.mp4"

    print(f"Creating video {output_file}")

    # get narration duration
    audio_duration = get_audio_duration(audio_file)

    # divide duration for 3 news
    img_duration = round(audio_duration / 3,2)
    

    command = [
        #"bin/ffmpeg.exe",
        "ffmpeg.exe"

        "-loop","1","-t",str(img_duration),"-i",img1,
        "-loop","1","-t",str(img_duration),"-i",img2,
        "-loop","1","-t",str(img_duration),"-i",img3,

        "-i",audio_file,
        "-i",music_file,

        "-filter_complex",
        "[0:v][1:v][2:v]concat=n=3:v=1:a=0,scale=1080:1920[v];"
        "[3:a][4:a]amix=inputs=2:duration=first:weights=1 0.35[a]",

        "-map","[v]",
        "-map","[a]",

        "-c:v","libx264",
        "-pix_fmt","yuv420p",
        "-y",
        output_file
    ]

    subprocess.run(command)

print("✅ Shorts videos generated")
