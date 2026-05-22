import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Setup
engine = create_engine("postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/accutane_db")
charts_path = r"C:\Users\16315\Desktop\Python\Projects\Accutane Database\charts"
processed_path = r"C:\Users\16315\Desktop\Python\Projects\Accutane Database\processed"

# Load data
df = pd.read_sql("SELECT * FROM reddit_nlp", engine)
df = df[df["cleaned_text"].notna() & (df["cleaned_text"] != "")]
print(f"Loaded {len(df)} posts for ML modeling")

# --- Model 1: K-Means Clustering ---
print("\n--- K-Means Clustering ---")
tfidf = TfidfVectorizer(max_features=500, stop_words="english")
X_tfidf = tfidf.fit_transform(df["cleaned_text"])

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_tfidf)

print("Cluster distribution:")
print(df["cluster"].value_counts())

# Show top terms per cluster
terms = tfidf.get_feature_names_out()
print("\nTop terms per cluster:")
for i, center in enumerate(kmeans.cluster_centers_):
    top_terms = [terms[j] for j in center.argsort()[-8:][::-1]]
    print(f"  Cluster {i}: {', '.join(top_terms)}")

# Cluster sentiment
cluster_sentiment = df.groupby("cluster")["sentiment_score"].mean()
print("\nAverage sentiment per cluster:")
print(cluster_sentiment)

# --- Model 2: Mental Health Mention Prediction (feature-based) ---
print("\n--- Mental Health Mention Prediction (feature-based) ---")

mental_health_terms = ["depression", "anxiety", "suicidal", "mood", "mental"]

def has_mental_health_mention(text):
    return int(any(term in str(text) for term in mental_health_terms))

df["mental_health_flag"] = df["cleaned_text"].apply(has_mental_health_mention)

print(f"Posts with mental health mentions: {df['mental_health_flag'].sum()}")
print(f"Posts without: {(df['mental_health_flag'] == 0).sum()}")

# Use only non-text features
feature_cols = ["sentiment_score", "score", "num_comments", "upvote_ratio"]
df_model = df[feature_cols + ["mental_health_flag"]].dropna()

X = df_model[feature_cols]
y = df_model["mental_health_flag"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

clf = LogisticRegression(max_iter=1000, class_weight="balanced")
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["no mention", "mental health mention"]))

# Feature importance
for name, coef in zip(feature_cols, clf.coef_[0]):
    print(f"  {name}: {coef:.4f}")

# --- Model 3: Topic Modeling (LDA) ---
print("\n--- Topic Modeling (LDA) ---")
lda = LatentDirichletAllocation(n_components=5, random_state=42)
lda.fit(X_tfidf)

print("Top terms per topic:")
for i, topic in enumerate(lda.components_):
    top_terms = [terms[j] for j in topic.argsort()[-8:][::-1]]
    print(f"  Topic {i}: {', '.join(top_terms)}")

# Save cluster results
df.to_csv(os.path.join(processed_path, "reddit_ml.csv"), index=False)

# Save cluster chart
fig, ax = plt.subplots(figsize=(8, 5))
cluster_counts = df["cluster"].value_counts().sort_index()
sns.barplot(x=cluster_counts.index, y=cluster_counts.values, palette="viridis", ax=ax)
ax.set_title("Reddit Post Clusters (K-Means)", fontsize=14)
ax.set_xlabel("Cluster")
ax.set_ylabel("Number of Posts")
plt.tight_layout()
plt.savefig(os.path.join(charts_path, "kmeans_clusters.png"), dpi=150)
plt.close()
print("\nSaved: kmeans_clusters.png")
print("Saved: reddit_ml.csv")