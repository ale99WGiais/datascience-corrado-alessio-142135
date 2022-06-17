
import os.path
from GoogleNews import GoogleNews
import requests
from tqdm import tqdm
import newspaper
import json
import pandas as pd
import os
import itertools

keywords = ["co2 emissions", "climate sentiment", "colorants chemical waste", "cosmetics waste", "cosmetics bio",
            "textiles bio", "textiles waste"]

if not os.path.exists("out"):
    os.mkdir("out")

googlenews = GoogleNews(lang="en", period="360d")

history = set()


for keyword in keywords:
    print(f"keyword: {keyword}")
    articles = []

    googlenews.get_news(keyword)
    links = googlenews.get_links()
    googlenews.clear()

    print(f"found {len(links)} links")

    for link in tqdm(links):
        try:
            url = f"https://{link}"

            article = newspaper.Article(url=url)
            article.download()
            article.parse()

            article ={
                "title": str(article.title),
                "text": str(article.text),
                "authors": article.authors,
                "published_date": str(article.publish_date),
                "top_image": str(article.top_image),
                "videos": article.movies,
                "keywords": article.keywords,
                "summary": str(article.summary)
            }

            articles.append(article)
        except Exception as e:
            print(f"EXCEPTION {e}")



    res = pd.DataFrame(data={
        "title": [a["title"] for a in articles],
        "text": [a["text"] for a in articles],
        "summary": [a["summary"] for a in articles],
        "keywords": [a["keywords"] for a in articles],
        "authors": [a["authors"] for a in articles]
    })

    res.to_csv(f"out/{keyword}.csv", index=False)



