import json
import pandas as pd
import argparse

def merge_json(file1, file2): 

    with open(file1, 'r') as f:
        data1 = json.load(f)

    with open(file2, 'r') as f:
        data2 = json.load(f)

    arts1 = data1.get("articles", [])
    arts2 = data2.get("articles", [])

    merged = arts1 + arts2

    return merged

def remove_duplicates(file, output):
    df = pd.DataFrame(file)
    df = df.drop_duplicates(subset="url", keep="first")

    with open(output, "w") as f:
        json.dump({"articles": df.to_dict(orient="records")}, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Fetch news articles from NewsAPI")

    parser.add_argument("--file1", type=str, required=True,
                        help="First file to merge")
    parser.add_argument("--file2", type=str, required=True,
                        help="Second file to merge")
    parser.add_argument("--output", type=str, required=True,
                        help="output path")

    args = parser.parse_args()

    file = merge_json(args.file1, args.file2)
    remove_duplicates(file, args.output)

if __name__ == "__main__":
    main()

    

