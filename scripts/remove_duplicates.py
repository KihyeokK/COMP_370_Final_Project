import json
import argparse


def remove_duplicates(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    articles = data.get("articles", [])
    seen_urls = set()
    unique_articles = []

    for article in articles:
        url = article.get("url")
        if url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)

    cleaned_data = {"articles": unique_articles}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

    print(f"Removed duplicates. New file saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Filter news articles")

    parser.add_argument("--input", type=str, required=True,
                        help="file to filter")
    parser.add_argument("--output", type=str, required=True,
                        help="filtered file")

    args = parser.parse_args()
    remove_duplicates(args.input, args.output)

if __name__ == "__main__":
    main()
