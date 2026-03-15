import os
import json
import requests

os.makedirs("images", exist_ok=True)

with open("data/filtered_news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

for i, item in enumerate(news):

    news_folder = f"images/news{i+1}"
    os.makedirs(news_folder, exist_ok=True)

    title = item["title"]
    query = "+".join(title.split()[:3])

    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={query}&gsrlimit=3&prop=imageinfo&iiprop=url&format=json"

    response = requests.get(url)
    data = response.json()

    if "query" not in data:
        print("No images found for", query)
        continue

    pages = data["query"]["pages"]

    count = 1

    for page in pages.values():

        img_url = page["imageinfo"][0]["url"]

        img_data = requests.get(img_url).content

        file_path = f"{news_folder}/img{count}.jpg"

        with open(file_path, "wb") as f:
            f.write(img_data)

        print("Downloaded", file_path)

        count += 1
