from PIL import Image, ImageDraw, ImageFont
import os
import json
import textwrap

input_folder = "news_images"
output_folder = "formatted_images"

os.makedirs(output_folder, exist_ok=True)

font_tag = ImageFont.truetype("Roboto-Bold.ttf", 45)
font_headline = ImageFont.truetype("Roboto-Bold.ttf", 70)

with open("data/filtered_news.json","r",encoding="utf-8") as f:
    news = json.load(f)

for i in range(1,10):

    img = Image.open(f"{input_folder}/news{i}.jpg").convert("RGBA")
    img = img.resize((1080,1920))

    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)

    # BREAKING TAG POSITION
    tag_top = 1700
    tag_bottom = 1765

    draw.rectangle((0,tag_top,420,tag_bottom), fill=(220,0,0,255))
    draw.text((20,tag_top+10),"BREAKING AI NEWS",font=font_tag,fill="white")

    # HEADLINE
    title = news[i-1]["title"]
    wrapped = textwrap.fill(title,width=22)
    lines = wrapped.split("\n")

    # calculate text height
    total_height = 0
    for line in lines:
        bbox = draw.textbbox((0,0),line,font=font_headline)
        total_height += bbox[3]-bbox[1] + 10

    headline_bottom = tag_top - 20
    headline_top = headline_bottom - total_height - 40

    # semi transparent black background
    draw.rectangle((0,headline_top,1080,headline_bottom), fill=(0,0,0,160))

    y = headline_top + 20

    for line in lines:
        bbox = draw.textbbox((0,0),line,font=font_headline)
        w = bbox[2]-bbox[0]
        h = bbox[3]-bbox[1]

        draw.text(((1080-w)/2,y),line,font=font_headline,fill="white")
        y += h + 10

    final = Image.alpha_composite(img, overlay)

    final.convert("RGB").save(f"{output_folder}/news{i}.jpg")

print("✅ Professional templates created")
