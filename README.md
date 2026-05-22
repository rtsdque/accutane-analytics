# Accutane (Isotretinoin) Treatment Outcomes — Healthcare Data Analytics Pipeline

A multi-source healthcare data analytics project analyzing real-world isotretinoin (Accutane) 
treatment outcomes using FDA adverse event data and patient-reported Reddit experiences.

Built as a portfolio centerpiece demonstrating an end-to-end analytics pipeline — from raw 
data collection through NLP, machine learning, and an interactive dashboard.

## Project Overview

Isotretinoin (commonly known as Accutane) is one of the most effective, and most 
controversial, treatments for severe acne. Despite widespread use, accessible and structured 
data on real-world patient outcomes remains limited. This project fills that gap by combining 
two independent data sources into a unified analytics pipeline.

**Research Questions:**
- What adverse reactions are most commonly reported by isotretinoin users?
- How does patient sentiment evolve across treatment months?
- Can machine learning identify distinct patient experience profiles?
- Is there a detectable signal connecting post engagement patterns to mental health content?

## Data Sources

### FDA FAERS (Food and Drug Administration Adverse Event Reporting System)
- 5 quarters of data: 2025 Q1 through 2026 Q1
- 4,061 unique isotretinoin adverse event reports
- 9,096 individual reaction entries across 1,234 unique reaction terms
- Filtered from 10+ million total FAERS drug records using isotretinoin brand name matching
- Tables collected: DRUG, REAC, DEMO, OUTC

### r/Accutane (Reddit)
- 5,005 posts collected via Arctic Shift archive
- Patient-reported treatment experiences, side effects, progress updates, and outcomes
- Covers a subreddit of 105,000+ members actively documenting isotretinoin treatment

**Why two sources?** FAERS captures formally reported adverse events — skewed negative by 
design, clinically grounded, and globally representative. Reddit captures the full patient 
experience spectrum — positive outcomes, side effect management, emotional journeys, and 
treatment timelines. Together they provide a more complete picture than either source alone.

## Tech Stack

| Layer | Tool |
|---|---|
| Database | PostgreSQL |
| Data Collection | Python, requests, Arctic Shift API |
| Data Processing | pandas |
| NLP | VADER, spaCy, NLTK |
| Machine Learning | scikit-learn |
| Visualization | matplotlib, seaborn, Plotly |
| Dashboard | Streamlit |
| Hosting | Railway + Streamlit Cloud |

## Pipeline Phases

### Phase 1 — Data Collection
- Downloaded FAERS quarterly ASCII files for 5 quarters
- Filtered 10+ million drug records to 5,506 isotretinoin-specific entries using brand name matching
- Collected linked REAC, DEMO, and OUTC records via primaryid join
- Scraped 5,005 r/Accutane posts via Arctic Shift API with pagination

### Phase 2 — Data Storage
- Designed a relational PostgreSQL schema mirroring FAERS table structure
- Loaded all 5 CSVs into accutane_db via SQLAlchemy
- Verified referential integrity through primaryid linking across tables

### Phase 3 — NLP Processing
- Combined post title and body into unified text field
- Cleaned text: removed URLs, punctuation, newlines, and extra whitespace
- Applied VADER sentiment analysis — scored all 5,005 posts on compound scale (-1 to +1)
- Built keyword extraction pipeline covering 27 side effect and outcome terms
- Extracted treatment month references via regex (validated range: months 1–12)

### Phase 4 — Exploratory Data Analysis
- Sentiment distribution: 46% positive, 39% negative, 15% neutral
- Top FAERS reactions: Depression (274), Dry skin (195), Arthralgia (188)
- Age distribution: median 22, mean 25 — consistent with expected Accutane demographics
- Sex breakdown: 73% female reporters, 27% male — reflects iPLEDGE monitoring patterns

### Phase 5 — Machine Learning
**K-Means Clustering (k=4)** on TF-IDF vectorized post text identified four natural patient groups:
- General Experience (3,046 posts) — everyday treatment discussion, slightly negative sentiment
- Progress Tracking (1,267 posts) — month-by-month documentation, positive sentiment (+0.20)
- Side Effects & Questions (414 posts) — focused side effect discussion, slightly negative
- Success Stories (278 posts) — treatment completion and results, strongest positive sentiment (+0.31)

**Mental Health Mention Detection** — Logistic regression classifier trained on behavioral 
features (sentiment score, upvote ratio, comment count) achieved 65% accuracy in detecting 
mental health content. Key finding: lower sentiment scores and higher comment counts 
significantly predict mental health mentions, suggesting community engagement patterns 
correlate with distress content.

**Topic Modeling (LDA, 5 topics)** surfaced five coherent themes: side effects, skin/acne 
progress, early treatment experience, emotional journey, and progress documentation.

### Phase 6 — Dashboard
Interactive Streamlit dashboard with five pages: Overview, FAERS Analysis, Reddit Sentiment, 
ML Insights, and About. Built with Plotly for interactive charts, custom dark theme, and 
contextual annotations throughout.

## Key Findings

1. **Depression is the third most reported adverse reaction in FAERS** — ranking above 
commonly expected physical side effects like dry skin and joint pain, with 274 reports 
across 5 quarters.

2. **Reddit sentiment is net positive** — 46% of posts scored positive vs 39% negative, 
suggesting that despite significant side effects, more patients report a net positive 
treatment experience than negative.

3. **Mental health content correlates with engagement** — posts mentioning depression, 
anxiety, or suicidal ideation attract significantly more comments, indicating the community 
rallies around distress content.

4. **Four distinct patient archetypes emerge** — K-Means clustering identified natural 
groupings that map closely to known Accutane patient behaviors: early struggle, progress 
tracking, side effect management, and post-treatment success.

5. **Pregnancy reporting dominates FAERS** — Exposure during pregnancy and unintended 
pregnancy are the top two reported reactions, reflecting mandatory iPLEDGE reporting 
requirements rather than treatment failure.

## Limitations

- FAERS captures adverse events only which systematically underrepresents positive outcomes
- Reddit data reflects self-selected patient voices and may not be demographically representative
- VADER sentiment analysis was designed for social media text but may misclassify medically 
nuanced posts
- Mental health prediction model achieves 65% accuracy — sufficient for pattern detection, 
not clinical application
- Treatment month analysis is limited by small sample sizes beyond month 6
- Combination drug entries (e.g. erythromycin/isotretinoin) were retained in collection 
and flagged for future filtering

## Disclaimer

This project is for academic research and portfolio purposes only. It does not constitute 
medical advice, clinical guidance, or endorsement of any treatment. All findings should be 
interpreted within the context of their data source limitations. Consult a licensed 
dermatologist or physician before making any treatment decisions.

## Built With

PostgreSQL · Python · pandas · VADER · scikit-learn · Streamlit · Plotly · Arctic Shift · FDA FAERS