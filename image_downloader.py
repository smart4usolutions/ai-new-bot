import json
import os
import requests
from bs4 import BeautifulSoup

with open("data/filtered_news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

os.makedirs("news_images", exist_ok=True)

for i, article in enumerate(news, start=1):

    article_url = article.get("url")

    if not article_url:
        print(f"No article url for news {i}")
        continue

    try:
        page = requests.get(article_url, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")

        # find og:image
        tag = soup.find("meta", property="og:image")

        if tag and tag.get("content"):

            image_url = tag["content"]

            img = requests.get(image_url, timeout=10)

            file_path = f"news_images/news{i}.jpg"

            with open(file_path, "wb") as f:
                f.write(img.content)

            print(f"Downloaded image for news {i}")

        else:
            print(f"No image found for news {i}, using default image")

            with open("assets/default_news.png", "rb") as f:
                default_img = f.read()

            with open(f"news_images/news{i}.jpg", "wb") as f:
                f.write(default_img)


    except Exception as e:
        print(f"Error processing news {i}: {e}")
