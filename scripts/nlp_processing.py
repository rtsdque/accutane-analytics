import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import nltk
from nltk.corpus import stopwords

# Load Reddit posts
df = pd.read_csv(r"C:\Users\16315\Desktop\Python\Projects\Accutane Database\processed\reddit_accutane.csv")

print(f"Loaded {len(df)} posts")
print(f"Columns: {df.columns.tolist()}")

# Combine title and selftext into one field
df["full_text"] = df["title"].fillna("") + " " + df["selftext"].fillna("")

# --- Step 1: Text Cleaning ---
def clean_text(text):
    text = str(text)
    text = re.sub(r"http\S+", "", text)        # remove URLs
    text = re.sub(r"\n", " ", text)            # remove newlines
    text = re.sub(r"[^\w\s]", "", text)        # remove punctuation
    text = re.sub(r"\s+", " ", text)           # remove extra spaces
    text = text.lower().strip()
    return text

df["cleaned_text"] = df["full_text"].apply(clean_text)

# --- Step 2: Sentiment Analysis ---
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    return scores["compound"]

def get_sentiment_label(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

df["sentiment_score"] = df["cleaned_text"].apply(get_sentiment)
df["sentiment_label"] = df["sentiment_score"].apply(get_sentiment_label)

# --- Step 3: Keyword Extraction ---
side_effects = [
    "dry lips", "chapped lips", "dry skin", "joint pain", "back pain",
    "depression", "anxiety", "mood", "suicidal", "hair loss", "hair thinning",
    "nosebleed", "dry eyes", "fatigue", "headache", "nausea", "rash",
    "sun sensitivity", "ib", "initial breakout", "purging", "acne",
    "clear", "clearing", "cleared", "relapse", "scarring"
]

def extract_keywords(text):
    found = [kw for kw in side_effects if kw in text]
    return ", ".join(found) if found else ""

df["keywords"] = df["cleaned_text"].apply(extract_keywords)

# --- Step 4: Extract Treatment Month ---
def extract_month(text):
    match = re.search(r"month\s*(\d+)", text)
    if match:
        return int(match.group(1))
    return None

df["treatment_month"] = df["cleaned_text"].apply(extract_month)

# Preview results
print("\nSentiment distribution:")
print(df["sentiment_label"].value_counts())
print("\nPosts with treatment month detected:")
print(df["treatment_month"].value_counts().head(10))
print("\nSample output:")
print(df[["title", "sentiment_score", "sentiment_label", "keywords", "treatment_month"]].head(10))

# Save enriched CSV
output_path = r"C:\Users\16315\Desktop\Python\Projects\Accutane Database\processed\reddit_nlp.csv"
df.to_csv(output_path, index=False)
print(f"\nSaved enriched dataset to {output_path}")

# Load into PostgreSQL
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://postgres:WindowsLaptop295@localhost:5432/accutane_db")
df.to_sql("reddit_nlp", engine, if_exists="replace", index=False)
print(f"Loaded {len(df)} rows into reddit_nlp table")