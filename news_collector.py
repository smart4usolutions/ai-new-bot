import requests
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
print("NEWS API KEY PRESENT:", bool(API_KEY))
if not API_KEY:
    print("❌ ERROR: NEWS_API_KEY Missing")
    exit(1)

yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

url = "https://newsapi.org/v2/top-headlines"

params = {
    #"q": "artificial intelligence OR Technology OR Science OR Global",
    "country": "us",
    # "from": yesterday,
    # "sortBy": "popularity",
    # "language": "en",
    # "pageSize": 50,
    "apiKey": API_KEY
}

response = requests.get(url, params=params)
articles = response.json()["articles"]

with open("data/raw_news.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, indent=2)

print("News saved successfully")
