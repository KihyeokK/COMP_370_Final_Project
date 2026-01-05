import json
import argparse
import re

ALLOWED_SOURCES = {
    "New York Post",
    "NBC News",
    "The New York Times",
    "The Atlantic",
    "New York Magazine",
    "Fox News",
    "Business Insider",
    "CBC News",
    "USA Today",
    "ABC News",
    "HuffPost",
    "The Intercept",
    "Gothamist",
    "The American Conservative"
}

# Regex for case-insensitive matching
PATTERN = re.compile(r"(mamdani|new york mayor)", re.IGNORECASE)

def filter_articles(input_file, output_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    filtered_articles = []

    for article in data["articles"]:
        source_name = article.get("source", {}).get("name", "")
        if source_name not in ALLOWED_SOURCES:
            continue  

        title = article.get("title", "") or ""
        description = article.get("description", "") or ""
        content = article.get("content", "") or ""

        if PATTERN.search(title) or PATTERN.search(description) or PATTERN.search(content):
            filtered_articles.append(article)

    output = {"articles": filtered_articles}

    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Kept {len(filtered_articles)} articles after filtering by source + Mamdani/NY mayor.")


def main():
    parser = argparse.ArgumentParser(description="Filter news articles")

    parser.add_argument("--input", type=str, required=True,
                        help="file to filter")
    parser.add_argument("--output", type=str, required=True,
                        help="filtered file")

    args = parser.parse_args()
    filter_articles(args.input, args.output)

if __name__ == "__main__":
    main()
