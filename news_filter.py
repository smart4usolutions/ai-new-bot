import json

with open("data/raw_news.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

seen_titles = set()
filtered = []

for article in articles:
    title = article["title"]

    if title not in seen_titles:
        seen_titles.add(title)

        filtered.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"]
        })

top10 = filtered[:3]

with open("data/filtered_news.json", "w", encoding="utf-8") as f:
    json.dump(top10, f, indent=2)

print("Top 10 news saved")
