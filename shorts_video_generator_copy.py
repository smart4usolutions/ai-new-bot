import os
import subprocess
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d")


audio_folder = "audio"
image_folder = "formatted_images"
assets_folder = "assets"
music_folder = "music"
output_folder = "videos"

os.makedirs(output_folder, exist_ok=True)

# 🎬 CHANGE TRANSITION HERE
TRANSITION_TYPE = "fade"  
# options:
# "fade"
# "slideleft"
# "smoothleft"
# "circleopen"

TRANSITION_DURATION = 0.5


def get_audio_duration(audio_file):
    result = subprocess.run(
        [
            #"bin/ffprobe.exe",
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_file
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)


# =====================================================
# 🧪 EXPERIMENTAL (1 NEWS = 1 SHORT)
# =====================================================

num_shorts = 9   # 🔥 dynamic
k=0
for i in range(1, 4):
    for j in range(1, 4):
        k+=1
        if (k > num_shorts):
            exit()
        img = f"{image_folder}/news{k}.jpg"
        audio = f"{audio_folder}/short{i}_voice{j}_{timestamp}.mp3"
        output = f"{output_folder}/exp_short{k}.mp4"

        print(img)
        print(audio)
        print(output)

        if not os.path.exists(audio) or not os.path.exists(img):
            print(f"❌ Missing file for experimental short {i}")
            continue

        duration = get_audio_duration(audio)

        command = [
            "bin/ffmpeg.exe",

            "-loop", "1", "-t", str(duration), "-i", img,
            "-i", audio,

            "-vf", "scale=1080:1920",

            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-shortest",
            "-y",
            output
        ]
        subprocess.run(command)
        print(f"✅ Experimental video created: {output}")
print(f"✅ Total Experimental video created: {k}")


# =====================================================
# 📰 REGULAR (3 NEWS = 1 SHORT)
# =====================================================

def create_3news_video(short_num, start_news_index):

    audios = [
        f"{audio_folder}/short{short_num}_voice1_{timestamp}.mp3",
        f"{audio_folder}/short{short_num}_voice2_{timestamp}.mp3",
        f"{audio_folder}/short{short_num}_voice3_{timestamp}.mp3"
    ]

    images = [
        f"{image_folder}/news{start_news_index}.jpg",
        f"{image_folder}/news{start_news_index+1}.jpg",
        f"{image_folder}/news{start_news_index+2}.jpg"
    ]

    transition_sound = f"{music_folder}/transition.mp3"
    transition_video = f"{assets_folder}/transition.mp4"
    output = f"{output_folder}/short{short_num}.mp4"

    # check files
    for f in audios + images:
        if not os.path.exists(f):
            print(f"❌ Missing file: {f}")
            return

    d1 = get_audio_duration(audios[0])
    d2 = get_audio_duration(audios[1])
    d3 = get_audio_duration(audios[2])

    # 🎬 offsets for transition
    offset1 = d1 - TRANSITION_DURATION
    offset2 = d1 + d2 - (TRANSITION_DURATION * 2)

    command = [
        "bin/ffmpeg.exe",

        # images
        "-loop", "1", "-t", str(d1), "-i", images[0],
        "-loop", "1", "-t", str(d2), "-i", images[1],
        "-loop", "1", "-t", str(d3), "-i", images[2],

        # audios
        "-i", audios[0],
        "-i", audios[1],
        "-i", audios[2],

        # transition sound
        "-i", transition_sound,

        "-i", "music/start_transition.mp4",   # [7:v]
        "-i", "music/transition.mp3",         # already [6:a]

        "-filter_complex",

        f"[0:v]scale=1080:1920,setsar=1[v0];"
        f"[1:v]scale=1080:1920,setsar=1[v1];"
        f"[2:v]scale=1080:1920,setsar=1[v2];"

        f"[7:v]chromakey=0x14FF1E:0.25:0.08,scale=1080:1920,setsar=1,setpts=PTS-STARTPTS[vstart];"

        f"[v0][vstart]overlay=shortest=1[v0t];"

        f"[v0t][v1]xfade=transition=fade:duration=0.5:offset={max(d1 - 0.5, 0)}[v01];"
        f"[v01][v2]xfade=transition=fade:duration=0.5:offset={max(d1 + d2 - 1.0, 0)}[v];"

        f"[3:a]adelay=0|0[a0];"
        f"[4:a]adelay={int(d1*1000)}|{int(d1*1000)}[a1];"
        f"[5:a]adelay={int((d1+d2)*1000)}|{int((d1+d2)*1000)}[a2];"

        f"[6:a]adelay={int(max((d1-0.5)*1000, 0))}|{int(max((d1-0.5)*1000, 0))}[t1];"
        f"[6:a]adelay={int(max((d1+d2-1.0)*1000, 0))}|{int(max((d1+d2-1.0)*1000, 0))}[t2];"

        f"[a0][a1][a2][t1][t2]amix=inputs=5:duration=longest[a];",

        "-map", "[v]",
        "-map", "[a]",

        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-y",
        output
    ]

    subprocess.run(command)
    print(f"✅ Created: {output}")


# Create 2 regular shorts
#create_3news_video(2, 4)  # news 4,5,6
#create_3news_video(3, 7)  # news 7,8,9

print("🎉 ALL VIDEOS GENERATED")
