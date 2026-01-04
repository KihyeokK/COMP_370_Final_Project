import argparse
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
COUNTRY = "us"
LANGUAGE = "en"
POLITICIAN = "Mamdani"

"""
This API allows only fetching 100 articles per request. 
I don't really understand how the date works, it looks like there are some overlaps when requesting different dates. 
It's not very reliable, we will have to clean the json files afterwads. 
The country parameter restricts the articles to US news, but not to North American NewsPapers. There are articles from other countries as well.
The politician parameter isn't very reliable either, we get articles that don't talk about Mamdani at all. Yet, they are all about us politics.
"""

def build_url(start_date):
    base = "https://newsapi.org/v2/everything?"
    url = (
        f"{base}"
        f"q={POLITICIAN}&"
        f"from={start_date}&"
        f"language={LANGUAGE}&"
        f"sortBy=popularity&"
        f"apiKey={API_KEY}"
    )
    return url


def fetch_articles(url, output_path):
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()

        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Saved {len(data.get('articles', []))} articles to {output_path}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching articles: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Fetch news articles from NewsAPI")

    parser.add_argument("--date", type=str, required=True,
                        help="Date in YYYY-MM-DD format")
    parser.add_argument("--output", type=str, required=True,
                        help="Output filename (e.g. articles.json)")

    args = parser.parse_args()

    output_dir = "/Users/antoninberanger/Documents/COMP370/final_project/data/"
    os.makedirs(output_dir, exist_ok=True)

    url = build_url(args.date)
    output_path = os.path.join(output_dir, args.output)

    fetch_articles(url, output_path)

if __name__ == "__main__":
    main()



