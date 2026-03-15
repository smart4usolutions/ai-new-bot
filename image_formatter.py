import os
import subprocess

input_folder = "news_images"
output_folder = "formatted_images"

os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):

    if file.endswith(".jpg") or file.endswith(".png"):

        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)

        command = [
            "ffmpeg",
            "-i", input_path,
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-y",
            output_path
        ]

        subprocess.run(command)

        print("Formatted:", file)
