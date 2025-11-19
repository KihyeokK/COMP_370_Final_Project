import requests
from bs4 import BeautifulSoup
import json
import time
import random


#polite scraping
def delay():
    time.sleep(2)

#chatgpt for request gets and to check if any error like: page 404 happens
def safe_request(url):
    try:
        delay()
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print("Warning:", r.status_code, "for", url)
            return None
        return r.text
    except Exception as e:
        print("Request failed:", e)
        return None

# where we will store the result
result = {"articles": []}

def scrape_nydailynews(max_pages=10):
    print("Scraping NYDailyNews across pages…")

    for page in range(1, max_pages + 1):
        url = f"https://www.nydailynews.com/page/{page}/?s=mamdani&orderby=date&order=desc"
        print(f"Page {page}: {url}")

        html = safe_request(url)
        if not html:
            break

        soup = BeautifulSoup(html, "html.parser")

        articles = soup.select("article.tag-search-view")
        if not articles:
            print("No more articles found: stopping.")
            break

        for art in articles:
            h2 = art.find("h2", class_="entry-title")
            if not h2:
                continue

            a = h2.find("a")
            if not a:
                continue

            title = a.get_text(strip=True)
            link = a.get("href")

            excerpt_div = art.find("div", class_="excerpt")
            description = excerpt_div.get_text(strip=True) if excerpt_div else ""

            result["articles"].append({
                "title": title,
                "description": description,
                "url": link
            })


#Run the scraper across pages 1–10
scrape_nydailynews(max_pages=10)

# Save JSON
with open("mamdani_nydailynews.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"Done — scraped {len(result['articles'])} articles.")
