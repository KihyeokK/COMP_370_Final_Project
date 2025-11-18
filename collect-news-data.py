import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_news_data(api_key, query, page_size=100):
    sources = 'cnn,nbc-news,national-review,new-scientist,newsweek,new-york-magazine,next-big-future,nfl-news,nhl-news,politico,polygon,recode,reddit-r-all,reuters,techcrunch,techradar,the-american-conservative,the-hill,the-huffington-post,the-next-web,the-verge,the-wall-street-journal,the-washington-post,the-washington-times,time,usa-today,wired'
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'language' : 'en',
        'sources': sources,
        'pageSize': page_size,
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None
if __name__ == "__main__":
    api_key = os.getenv('API_KEY')
    query = 'zohran mamdani'
    news_data = fetch_news_data(api_key, query)
    if news_data:
        with open('news_data.json', 'w') as f:
            json.dump(news_data, f, indent=4)
        print("News data saved to news_data.json")
    else:
        print("Failed to fetch news data.")
        print(news_data)
