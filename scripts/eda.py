import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

# Setup
engine = create_engine("postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/accutane_db")
output_path = r"C:\Users\16315\Desktop\Python\Projects\Accutane Database\charts"
os.makedirs(output_path, exist_ok=True)

sns.set_theme(style="darkgrid")

# --- Load data ---
df_reac = pd.read_sql("SELECT * FROM faers_reac", engine)
df_demo = pd.read_sql("SELECT * FROM faers_demo", engine)
df_drug = pd.read_sql("SELECT * FROM faers_drug", engine)
df_reddit = pd.read_sql("SELECT * FROM reddit_nlp", engine)

# --- Deduplicate FAERS by keeping highest caseversion ---
df_demo_dedup = df_demo.sort_values("caseversion", ascending=False).drop_duplicates(subset="primaryid")
print(f"FAERS demo before dedup: {len(df_demo)} | after: {len(df_demo_dedup)}")

# --- Fix treatment month (only accept 1-12) ---
df_reddit["treatment_month"] = pd.to_numeric(df_reddit["treatment_month"], errors="coerce")
df_reddit_months = df_reddit[df_reddit["treatment_month"].between(1, 12)]

# --- Chart 1: Sentiment Distribution ---
fig, ax = plt.subplots(figsize=(8, 5))
order = ["positive", "negative", "neutral"]
colors = ["#2ecc71", "#e74c3c", "#95a5a6"]
sentiment_counts = df_reddit["sentiment_label"].value_counts().reindex(order)
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette=colors, ax=ax)
ax.set_title("Reddit Post Sentiment Distribution", fontsize=14)
ax.set_xlabel("Sentiment")
ax.set_ylabel("Number of Posts")
for i, v in enumerate(sentiment_counts.values):
    ax.text(i, v + 20, str(v), ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(output_path, "sentiment_distribution.png"), dpi=150)
plt.close()
print("Saved: sentiment_distribution.png")

# --- Chart 2: Top 20 FAERS Reactions ---
top_reactions = df_reac["pt"].value_counts().head(20)
fig, ax = plt.subplots(figsize=(10, 7))
sns.barplot(x=top_reactions.values, y=top_reactions.index, palette="Reds_r", ax=ax)
ax.set_title("Top 20 Adverse Reactions (FAERS)", fontsize=14)
ax.set_xlabel("Report Count")
ax.set_ylabel("Reaction")
plt.tight_layout()
plt.savefig(os.path.join(output_path, "top_reactions_faers.png"), dpi=150)
plt.close()
print("Saved: top_reactions_faers.png")

# --- Chart 3: Sentiment by Treatment Month ---
month_sentiment = df_reddit_months.groupby("treatment_month")["sentiment_score"].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=month_sentiment, x="treatment_month", y="sentiment_score", marker="o", color="#3498db", ax=ax)
ax.axhline(0, color="gray", linestyle="--", alpha=0.5)
ax.set_title("Average Sentiment Score by Treatment Month", fontsize=14)
ax.set_xlabel("Treatment Month")
ax.set_ylabel("Average Sentiment Score")
ax.set_xticks(range(1, 13))
plt.tight_layout()
plt.savefig(os.path.join(output_path, "sentiment_by_month.png"), dpi=150)
plt.close()
print("Saved: sentiment_by_month.png")

# --- Chart 4: Age Distribution ---
df_demo_clean = df_demo_dedup[df_demo_dedup["age"].between(10, 60)]
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df_demo_clean["age"], bins=30, color="#9b59b6", kde=True, ax=ax)
ax.set_title("Patient Age Distribution (FAERS)", fontsize=14)
ax.set_xlabel("Age")
ax.set_ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(output_path, "age_distribution.png"), dpi=150)
plt.close()
print("Saved: age_distribution.png")

# --- Chart 5: Top Reddit Keywords ---
all_keywords = df_reddit["keywords"].dropna().str.split(", ").explode()
all_keywords = all_keywords[all_keywords != ""]
keyword_counts = all_keywords.value_counts().head(15)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=keyword_counts.values, y=keyword_counts.index, palette="Blues_r", ax=ax)
ax.set_title("Top 15 Side Effect Keywords (Reddit Posts)", fontsize=14)
ax.set_xlabel("Mention Count")
ax.set_ylabel("Keyword")
plt.tight_layout()
plt.savefig(os.path.join(output_path, "reddit_keywords.png"), dpi=150)
plt.close()
print("Saved: reddit_keywords.png")

print("\nAll charts saved to charts folder.")