import json
import argparse

def restructure_json(input_file, output_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    filtered = {
        "articles": []
    }

    for article in data.get("articles", []):
        filtered_article = {
            "id": article["source"].get("id"),
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url")
        }
        filtered["articles"].append(filtered_article)

    with open(output_file, "w") as f:
        json.dump(filtered, f, indent=2)
    
def main():
    parser = argparse.ArgumentParser(description="Fetch news articles from NewsAPI")

    parser.add_argument("--input", type=str, required=True,
                        help="input JSON")
    parser.add_argument("--output", type=str, required=True,
                        help="output JSON")

    args = parser.parse_args()
    restructure_json(args.input, args.output)

if __name__ == "__main__":
    main()