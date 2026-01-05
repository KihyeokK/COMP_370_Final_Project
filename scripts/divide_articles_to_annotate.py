import csv
import random
import argparse

def divide_tsv_corpus(input_filename, output, num_coders=3):
    try:
        with open(input_filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)
    except:
        print("Error reading input TSV.")
        return

    if not rows:
        print("No articles found.")
        return

    random.shuffle(rows)
    chunk_size = (len(rows) + num_coders - 1) // num_coders

    for i in range(num_coders):
        start = i * chunk_size
        end = start + chunk_size
        chunk = rows[start:end]

        if not chunk:
            continue

        output = f"{output}{i+1}.tsv"
        with open(output, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "title", "description", "coding"], delimiter="\t")
            writer.writeheader()
            for row in chunk:
                writer.writerow({
                    "id": row.get("id", "N/A"),
                    "title": row.get("title", "N/A"),
                    "description": row.get("description", "N/A"),
                    "coding": row.get("coding", "")
                })

        print(f"Saved {len(chunk)} to {output}")

    print("Done.")

def main():
    parser = argparse.ArgumentParser(description="Generate media bias distribution pie chart")
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()
    divide_tsv_corpus(args.input, args.output, 3)

if __name__ == "__main__":
    main()
