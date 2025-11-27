import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


PATH = r"C:\Users\saleh\COMP370_final_project\COMP_370_Final_Project\data\final_full_annotated.csv" 
df = pd.read_csv(PATH)

#the "coding" column is the topic label
topic_col = "coding"

# combine title + description into a single text field
df["text"] = df["title"].fillna("") + " " + df["description"].fillna("")

#For each topic, compute TF-IDF on all its articles
top_n = 20  # how many top words to show per topic

for topic, group in df.groupby(topic_col):
    print("=" * 80)
    print(f"TOPIC: {topic}")
    print("=" * 80)

    texts = group["text"].tolist()

    # create a fresh TF-IDF vectorizer for THIS topic’s corpus
    vectorizer = TfidfVectorizer(
        stop_words="english",   # drop common English words
        max_df=0.9,             # ignore super-common words within this topic
        min_df=2                # keep words that appear in at least 2 docs
    )
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()

    # average TF-IDF score of each word across all docs in this topic
    avg_scores = tfidf_matrix.mean(axis=0).A1  # convert to 1D array

    # get indices of top N words
    top_indices = avg_scores.argsort()[::-1][:top_n]

    # print them nicely
    for idx in top_indices:
        word = feature_names[idx]
        score = avg_scores[idx]
        print(f"{word:20s} {score:.4f}")

    print("\n")
