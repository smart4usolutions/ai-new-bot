import json
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import shutil

# ----------------------------
# CONFIG
# ----------------------------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

DEFAULT_IMAGE_PATH = "assets/default_news.png"
OUTPUT_FOLDER = "news_images"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ----------------------------
# LOAD NEWS
# ----------------------------
with open("data/filtered_news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

# ----------------------------
# FUNCTION: VALIDATE IMAGE
# ----------------------------
def is_valid_image(content):
    try:
        img = Image.open(BytesIO(content))
        img.verify()  # check if valid image
        return True
    except Exception:
        return False

# ----------------------------
# MAIN LOOP
# ----------------------------
for i, article in enumerate(news, start=1):

    file_path = f"{OUTPUT_FOLDER}/news{i}.jpg"
    article_url = article.get("url")

    try:
        # ----------------------------
        # STEP 1: FETCH ARTICLE PAGE
        # ----------------------------
        if not article_url:
            raise Exception("No article URL")

        page = requests.get(article_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")

        # ----------------------------
        # STEP 2: GET IMAGE URL
        # ----------------------------
        tag = soup.find("meta", property="og:image")

        if not tag or not tag.get("content"):
            raise Exception("No og:image found")

        image_url = tag["content"]

        # ----------------------------
        # STEP 3: DOWNLOAD IMAGE
        # ----------------------------
        img_response = requests.get(image_url, headers=HEADERS, timeout=10)

        if img_response.status_code != 200:
            raise Exception("Image download failed")

        # ----------------------------
        # STEP 4: VALIDATE IMAGE
        # ----------------------------
        if not is_valid_image(img_response.content):
            raise Exception("Invalid image content")

        # ----------------------------
        # STEP 5: SAVE IMAGE
        # ----------------------------
        with open(file_path, "wb") as f:
            f.write(img_response.content)

        print(f"✅ Downloaded valid image for news {i}")

    except Exception as e:
        print(f"⚠️ Error for news {i}: {e}")
        print(f"🖼️ Using default image for news {i}")

        try:
            shutil.copy(DEFAULT_IMAGE_PATH, file_path)
        except Exception as copy_error:
            print(f"❌ Failed to copy default image: {copy_error}")
