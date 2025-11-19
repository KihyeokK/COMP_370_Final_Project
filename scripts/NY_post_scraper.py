import requests
from bs4 import BeautifulSoup
import json
import time

def delay():
    time.sleep(2)

#chatgpt, to block the error we get (it works!)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}

def safe_request(url):
    try:
        delay()
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200:
            print("Warning:", r.status_code, "for", url)
            return None
        return r.text
    except Exception as e:
        print("Request failed:", e)
        return None

result = {"articles": []}

def scrape_nypost(max_pages=20):
    print("Scraping NYPost…")

    base = "https://nypost.com/search/mamdani"

    for page in range(1, max_pages + 1):

        if page == 1:
            url = base + "/"
        else:
            url = f"{base}/page/{page}/"

        print(f"Page {page}: {url}")

        html = safe_request(url)
        if not html:
            break

        soup = BeautifulSoup(html, "html.parser")

        cards = soup.select("div.search-results__story")
        if not cards:
            print("No more articles — stopping.")
            break

        for card in cards:

            # Title & URL
            a = card.select_one("h3.story__headline a")
            if not a:
                continue

            title = a.get_text(strip=True)
            url = a.get("href").strip()

            # Description
            p = card.select_one("p.story__excerpt")
            description = p.get_text(strip=True) if p else ""

            result["articles"].append({
                "title": title,
                "description": description,
                "url": url
            })


scrape_nypost(max_pages=20)

with open("mamdani_nypost.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"Done: scraped {len(result['articles'])} NYPost articles.")
