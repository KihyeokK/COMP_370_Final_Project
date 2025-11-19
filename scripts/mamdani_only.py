import json

input_file = r"C:\Users\saleh\COMP370_final_project\data\mamdani_nydailynews.json"      
output_file = "mamdani_filtered_nydaily.json"     

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

filtered = {
    "articles": [
        article for article in data["articles"]
        if "mamdani" in article["title"].lower()
    ]
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(filtered, f, indent=2, ensure_ascii=False)

print(f"Done. Kept {len(filtered['articles'])} articles containing 'mamdani'.")
