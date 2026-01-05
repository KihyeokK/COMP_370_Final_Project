import json
import csv
import argparse

def convert_json_to_tsv(input_filename, output_filename):
    try:
        with open(input_filename, "r", encoding="utf-8") as f:
            articles = json.load(f).get("articles", [])
    except:
        print("Error: Cannot open or parse input JSON.")
        return

    if not articles:
        print("No articles found.")
        return

    fieldnames = ["id", "title", "description", "coding"]

    with open(output_filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for a in articles:
            writer.writerow({
                "id": a.get("id", "N/A"),
                "title": a.get("title", "N/A"),
                "description": a.get("description", "N/A"),
                "coding": ""
            })

    print(f"Saved {len(articles)} rows to {output_filename}")

def main():
    parser = argparse.ArgumentParser(description="Generate media bias distribution pie chart")
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()
    convert_json_to_tsv(args.input, args.output)

if __name__ == "__main__":
    main()
