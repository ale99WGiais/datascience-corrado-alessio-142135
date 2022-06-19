
import os.path
from GoogleNews import GoogleNews
import requests
from tqdm import tqdm
import newspaper
import json
import pandas as pd
import os
import itertools


keywords = {
    "sustainability": ["co2 emissions", "climate sentiment", "climate change", "pollution", "waste", "co2", "sustainability",
                       "eu sustainability", "co2 credits", "co2 good", "co2 bad", "co2 issues"],
    "chemical colorants": ["colorants", "chemical colorants", "chemical dye", "textile colorants", "cosmetic colorants", "colorants waste",
                           "use of colorants", "colorants industry", "textiles colorants waste", "cosmetics colorants waste",
                           "chemical colorants good", "chemical colorants bad", "chemical colorants issues"],
    "spirulina": ["spirulina", "spirulina cultivation", "spirulina microalgae", "spirulina italy", "spirulina sustainability",
                  "spirulina photobioreactor", "spirulina colorants", "spirulina good", "spirulina bad", "spirulina issues"],
    "phycocyanin": ["phycocyanin", "spirulina phycocyanin", "phycocyanin sentiment", "phycocyanin opinion", "phycocyanin textiles",
                    "phycocyanin cosmetics", "phycocyanin dye", "phycocyanin use", "phycocyanin opinion", "phycocyanin good", "phycocyanin bad",
                    "phycocyanin issues"],
    "steel production": ["steel production", "steel production emissions", "steel production co2", "steel production sentiment",
                         "steel production opinion", "steel production sustainability", "steel production good", "steel production bad",
                         "steel production issues"]
}

if not os.path.exists("out"):
    os.mkdir("out")

googlenews = GoogleNews(lang="en", period="360d")


for theme, keywords in keywords.items():
    print(f"theme {theme}")

    df_keywords = []
    articles = []

    for keyword in keywords:
        print(f"keyword: {keyword}")

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
                df_keywords.append(keyword)
            except Exception as e:
                print(f"EXCEPTION {e}")

    res = pd.DataFrame(data={
        "theme": theme,
        "keywords": df_keywords,
        "title": [a["title"] for a in articles],
        "text": [a["text"] for a in articles],
        "summary": [a["summary"] for a in articles],
        "authors": [a["authors"] for a in articles]
    })

    res.to_csv(f"out/{theme}.csv", index=False)



