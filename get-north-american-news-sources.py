import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_news_sources(api_key, country='us'):
    url = 'https://newsapi.org/v2/sources'
    params = {
        'country': country,
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        sources_data = response.json()
        sources = [source['id'] for source in sources_data['sources']]
        return ','.join(sources)
    else:
        print(f"Error: {response.status_code}")
        return None
if __name__ == "__main__":
    api_key = os.getenv('API_KEY')
    north_american_sources = fetch_news_sources(api_key, country='us')
    if north_american_sources:
        with open('north_american_news_sources.txt', 'w') as f:
            f.write(north_american_sources)
        print("North American news sources saved to north_american_news_sources.txt")
    else:
        print("Failed to fetch North American news sources.")
