import pandas as pd

df = pd.read_csv("final_full_annotated.csv")

# Combine title + description into a single text field
df["text"] = df["title"].fillna("") + " " + df["description"].fillna("")
df["text"] = df["text"].str.replace("New York", "New_York", regex=False)
df["text"] = df["text"].str.replace("new york", "New_York", regex=False)
df["coding"] = df["coding"].astype(str)

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1, 2)   # include 1-word and 2-word tokens
)
X = vectorizer.fit_transform(df["text"])
terms = vectorizer.get_feature_names_out()

import numpy as np

results = {}

for cat in df["coding"].unique():
    idx = df["coding"] == cat
    if idx.sum() == 0:
        continue
    
    # average TF-IDF vector for that category
    mean_vec = X[idx.to_numpy()].mean(axis=0).A1
    
    # get top 10 indices
    top_idx = mean_vec.argsort()[::-1][:10]
    top_words = [terms[i] for i in top_idx]
    
    results[cat] = top_words

for cat, words in results.items():
    print(f"\n=== {cat} ===")
    for w in words:
        print("-", w)

    # Save to file
with open("tfidf_top_words.txt", "w") as f:
    for cat, words in results.items():
        f.write(f"\n{cat}\n")
        for w in words:
            f.write(f"- {w}\n")
