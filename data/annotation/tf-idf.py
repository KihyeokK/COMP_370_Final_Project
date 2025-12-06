import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("final_full_annotated.csv")

# Combine title + description into a single text field
df["text"] = df["title"].fillna("") + " " + df["description"].fillna("")
df["text"] = df["text"].str.replace("New York", "New_York", regex=False)
df["text"] = df["text"].str.replace("new york", "New_York", regex=False)
df["coding"] = df["coding"].astype(str)

vectorizer = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1, 2) # include 1-word and 2-word tokens, unigram + bigrams
)
X = vectorizer.fit_transform(df["text"]) # TF-IDF matrix
terms = vectorizer.get_feature_names_out()

import numpy as np

results = {}

for cat in df["coding"].unique():
    idx = df["coding"] == cat
    if idx.sum() == 0:
        continue
    
    # average TF-IDF vector for that category
    mean_vec = X[idx.to_numpy()].mean(axis=0).A1 # pick the rows for that category and average them
    
    # get top 10 indices
    top_idx = mean_vec.argsort()[::-1][:10]
    top_words = [terms[i] for i in top_idx]
    
    # also, store the actual tf-idf scores
    top_scores = [mean_vec[i] for i in top_idx]
    results[cat] = (top_words, top_scores)

print(results)

for cat, (words, scores) in results.items():
    print(f"\n=== {cat} ===")
    for w, s in zip(words, scores):
        print(f"- {w}: {s}")

with open("tfidf_top_words.txt", "w") as f:
    for cat, (words, scores) in results.items():
        f.write(f"\n{cat}\n")
        for w, s in zip(words, scores):
            f.write(f"- {w}: {s}\n")

# figure for tf-idf results
for cat, (words, scores) in results.items():
    plt.figure(figsize=(10, 6))
    plt.barh(words[::-1], scores[::-1], color='skyblue')
    plt.xlabel("Average TF-IDF Score")
    plt.title(f"Top TF-IDF Words for Category: {cat}")
    plt.tight_layout()
    plt.savefig(f"tfidf_{cat.replace(' ', '_')}.png")
    plt.close()

# a table figure plot for tf-idf results
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')
table_data = []
for cat, (words, scores) in results.items():
    table_data.append([cat] + words)
table = ax.table(cellText=table_data, colLabels=["Category"] + [f"Top {i+1}" for i in range(10)], cellLoc='left', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.5, 4)
plt.title("Top TF-IDF Words by Category", fontsize=14)
plt.savefig("tfidf_top_words_table.png", bbox_inches='tight')
plt.close()
