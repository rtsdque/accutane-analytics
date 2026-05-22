import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# --- Page Config ---
st.set_page_config(
    page_title="Accutane Treatment Analytics",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Database Connection ---
@st.cache_resource
def get_engine():
    return create_engine("postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/accutane_db")

engine = get_engine()

@st.cache_data
def load_data():
    df_reac = pd.read_sql("SELECT * FROM faers_reac", engine)
    df_demo = pd.read_sql("SELECT * FROM faers_demo", engine)
    df_drug = pd.read_sql("SELECT * FROM faers_drug", engine)
    df_reddit = pd.read_sql("SELECT * FROM reddit_nlp", engine)
    df_ml = pd.read_sql("SELECT * FROM reddit_ml", engine)
    return df_reac, df_demo, df_drug, df_reddit, df_ml

df_reac, df_demo, df_drug, df_reddit, df_ml = load_data()

# --- Global Styling ---
st.markdown("""
<style>
.stApp {
    background-color: #0a0a0f;
    color: #e0e0e0;
}
[data-testid="stSidebar"] {
    background-color: #0d0d1a;
    border-right: 1px solid #1e1e3a;
}
.metric-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #0f3460;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin: 8px 0;
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: #4fc3f7;
}
.metric-label {
    font-size: 0.85rem;
    color: #90a4ae;
    margin-top: 4px;
}
h1, h2, h3 {
    color: #4fc3f7 !important;
}
.disclaimer {
    background-color: #1a1a0a;
    border-left: 4px solid #f39c12;
    padding: 12px 16px;
    border-radius: 4px;
    font-size: 0.85rem;
    color: #bdbdbd;
    margin: 16px 0;
}
</style>
""", unsafe_allow_html=True)

# --- Shared chart layout defaults ---
def base_layout():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=13, color="#e0e0e0"),
        hoverlabel=dict(
            bgcolor="#1a1a2e",
            bordercolor="#4fc3f7",
            font_size=13,
            font_color="#e0e0e0"
        )
    )

# --- Sidebar ---
st.sidebar.markdown("## 💊 Accutane Analytics")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", ["Overview", "FAERS Analysis", "Reddit Sentiment", "ML Insights", "About"])
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size:0.75rem; color:#546e7a;'>
Data Sources: FDA FAERS + r/Accutane<br>
Quarters: 2025 Q1 — 2026 Q1<br>
Posts: 5,005 | Reports: 4,061
</div>
""", unsafe_allow_html=True)

# =====================
# PAGE: OVERVIEW
# =====================
if page == "Overview":
    st.title("Accutane Treatment Outcomes Dashboard")
    st.markdown("#### A multi-source healthcare analytics project combining FDA adverse event data with patient-reported experiences.")
    st.markdown('<div class="disclaimer">⚠️ This dashboard is for research and educational purposes only. It does not constitute medical advice. Always consult a licensed healthcare provider before making treatment decisions.</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">4,061</div><div class="metric-label">FAERS Reports</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">9,096</div><div class="metric-label">Adverse Reactions</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">5,005</div><div class="metric-label">Reddit Posts</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-value">1,234</div><div class="metric-label">Unique Reactions</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Sentiment Distribution (Reddit)")
        sentiment_counts = df_reddit["sentiment_label"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentiment", "Count"]
        sentiment_counts["Sentiment"] = sentiment_counts["Sentiment"].str.capitalize()
        color_map = {"Positive": "#2ecc71", "Negative": "#e74c3c", "Neutral": "#95a5a6"}
        fig = px.bar(sentiment_counts, x="Sentiment", y="Count",
                     color="Sentiment", color_discrete_map=color_map,
                     template="plotly_dark")
        fig.update_traces(hovertemplate="<b>Sentiment:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>")
        fig.update_layout(showlegend=False, **base_layout())
        st.plotly_chart(fig, use_container_width=True)
        st.caption("46% of r/Accutane posts scored positive sentiment, compared to 39% negative and 15% neutral — suggesting that despite significant side effects, more patients report a net positive treatment experience than negative.")

    with col_r:
        st.subheader("Top 10 Adverse Reactions (FAERS)")
        top_reac = df_reac["pt"].value_counts().head(10).reset_index()
        top_reac.columns = ["Reaction", "Count"]
        fig2 = px.bar(top_reac, x="Count", y="Reaction", orientation="h",
                      color="Count", color_continuous_scale="Reds",
                      template="plotly_dark")
        fig2.update_traces(hovertemplate="<b>Reaction:</b> %{y}<br><b>Count:</b> %{x}<extra></extra>")
        fig2.update_layout(showlegend=False, yaxis=dict(autorange="reversed"),
                           coloraxis_showscale=False, **base_layout())
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Depression ranks third among all reported reactions, above commonly expected physical side effects like dry skin and joint pain — highlighting the psychiatric burden associated with isotretinoin treatment.")

# =====================
# PAGE: FAERS ANALYSIS
# =====================
elif page == "FAERS Analysis":
    st.title("FAERS Clinical Data Analysis")
    st.markdown("FDA Adverse Event Reporting System — isotretinoin reports from 2025 Q1 through 2026 Q1.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Patient Age Distribution")
        df_demo_clean = df_demo[df_demo["age"].between(10, 60)].copy()
        fig = px.histogram(df_demo_clean, x="age", nbins=30,
                           color_discrete_sequence=["#9b59b6"],
                           template="plotly_dark",
                           labels={"age": "Age", "count": "Count"})
        fig.update_traces(hovertemplate="<b>Age:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>")
        fig.update_layout(xaxis_title="Age", yaxis_title="Count", **base_layout())
        st.plotly_chart(fig, use_container_width=True)
        st.caption("The median patient age is 22, consistent with isotretinoin's primary use in adolescent and young adult acne treatment. The long tail toward older ages reflects off-label and adult-onset acne use cases.")

    with col2:
        st.subheader("Reports by Sex")
        sex_counts = df_demo[df_demo["sex"].isin(["F", "M"])]["sex"].value_counts().reset_index()
        sex_counts.columns = ["Sex", "Count"]
        sex_counts["Sex"] = sex_counts["Sex"].map({"F": "Female", "M": "Male"})
        fig2 = px.pie(sex_counts, names="Sex", values="Count",
                      color_discrete_sequence=["#4fc3f7", "#f06292"],
                      template="plotly_dark", hole=0.4)
        fig2.update_traces(hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>")
        fig2.update_layout(**base_layout())
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("73% of reports come from female patients, reflecting both isotretinoin's demographics and the stricter iPLEDGE monitoring requirements for females of childbearing potential, which increases reporting frequency.")

    st.subheader("Top 20 Adverse Reactions")
    top_reac20 = df_reac["pt"].value_counts().head(20).reset_index()
    top_reac20.columns = ["Reaction", "Count"]
    fig3 = px.bar(top_reac20, x="Count", y="Reaction", orientation="h",
                  color="Count", color_continuous_scale="Reds",
                  template="plotly_dark")
    fig3.update_traces(hovertemplate="<b>Reaction:</b> %{y}<br><b>Count:</b> %{x}<extra></extra>")
    fig3.update_layout(yaxis=dict(autorange="reversed"), height=600,
                       coloraxis_showscale=False, **base_layout())
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Pregnancy-related entries dominate the top reactions due to mandatory iPLEDGE reporting requirements — not treatment failure. Excluding these, depression (274 reports), dry skin (195), and arthralgia (188) represent the most clinically significant findings.")

# =====================
# PAGE: REDDIT SENTIMENT
# =====================
elif page == "Reddit Sentiment":
    st.title("Reddit Sentiment Analysis")
    st.markdown("Patient-reported experiences from r/Accutane — 5,005 posts analyzed.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sentiment by Treatment Month")
        df_months = df_reddit[df_reddit["treatment_month"].between(1, 12)].copy()
        month_sentiment = df_months.groupby("treatment_month")["sentiment_score"].agg(["mean", "count"]).reset_index()
        month_sentiment.columns = ["Month", "Avg Sentiment", "Post Count"]
        fig = px.line(month_sentiment, x="Month", y="Avg Sentiment",
                      markers=True, template="plotly_dark",
                      color_discrete_sequence=["#4fc3f7"],
                      custom_data=["Post Count"])
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        fig.update_traces(hovertemplate="<b>Month:</b> %{x}<br><b>Avg Sentiment:</b> %{y:.3f}<br><b>Posts:</b> %{customdata[0]}<extra></extra>")
        fig.update_layout(xaxis=dict(tickmode="linear", dtick=1, title="Treatment Month"),
                          yaxis_title="Avg Sentiment Score", **base_layout())
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Sentiment peaks positively in month 2 before dipping sharply in months 3–4, consistent with the well-documented initial breakout period. Note: data beyond month 6 is sparse — treat late-month trends cautiously.")

    with col2:
        st.subheader("Top Keywords in Posts")
        all_keywords = df_reddit["keywords"].dropna().str.split(", ").explode()
        all_keywords = all_keywords[all_keywords != ""]
        kw_counts = all_keywords.value_counts().head(15).reset_index()
        kw_counts.columns = ["Keyword", "Count"]
        fig2 = px.bar(kw_counts, x="Count", y="Keyword", orientation="h",
                      color="Count", color_continuous_scale="Blues",
                      template="plotly_dark")
        fig2.update_traces(hovertemplate="<b>Keyword:</b> %{y}<br><b>Count:</b> %{x}<extra></extra>")
        fig2.update_layout(yaxis=dict(autorange="reversed"),
                           coloraxis_showscale=False, **base_layout())
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("'Acne' and 'ib' (initial breakout) dominate keyword mentions, followed by 'clear' — reflecting the central tension of isotretinoin treatment: a difficult start followed by skin clearing for most patients.")

    st.subheader("Explore Posts")
    sentiment_filter = st.selectbox("Filter by Sentiment", ["All", "Positive", "Negative", "Neutral"])
    if sentiment_filter != "All":
        df_filtered = df_reddit[df_reddit["sentiment_label"] == sentiment_filter.lower()]
    else:
        df_filtered = df_reddit
    display_df = df_filtered[["title", "sentiment_label", "sentiment_score", "keywords", "treatment_month"]].copy()
    display_df.columns = ["Title", "Sentiment", "Score", "Keywords", "Treatment Month"]
    display_df["Sentiment"] = display_df["Sentiment"].str.capitalize()
    st.dataframe(display_df.head(50), use_container_width=True)

# =====================
# PAGE: ML INSIGHTS
# =====================
elif page == "ML Insights":
    st.title("Machine Learning Insights")

    cluster_labels = {
        0: "General Experience",
        1: "Side Effects & Questions",
        2: "Success Stories",
        3: "Progress Tracking"
    }
    df_ml["Cluster"] = df_ml["cluster"].map(cluster_labels)

    st.subheader("K-Means Patient Clusters")
    cluster_counts = df_ml["Cluster"].value_counts().reset_index()
    cluster_counts.columns = ["Cluster", "Count"]
    fig = px.bar(cluster_counts, x="Cluster", y="Count",
                 color="Cluster", template="plotly_dark",
                 color_discrete_sequence=["#4fc3f7", "#f06292", "#2ecc71", "#f39c12"])
    fig.update_traces(hovertemplate="<b>Cluster:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>")
    fig.update_layout(showlegend=False, **base_layout())
    st.plotly_chart(fig, use_container_width=True)
    st.caption("K-Means clustering on post text identified four natural patient archetypes. The General Experience cluster dominates, reflecting the broad range of everyday treatment discussion on r/Accutane.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Cluster Sentiment")
        cluster_sent = df_ml.groupby("Cluster")["sentiment_score"].mean().reset_index()
        cluster_sent.columns = ["Cluster", "Avg Sentiment Score"]
        fig2 = px.bar(cluster_sent, x="Cluster", y="Avg Sentiment Score",
                      color="Avg Sentiment Score",
                      color_continuous_scale="RdYlGn",
                      template="plotly_dark")
        fig2.update_traces(hovertemplate="<b>Cluster:</b> %{x}<br><b>Avg Sentiment:</b> %{y:.3f}<extra></extra>")
        fig2.update_layout(coloraxis_showscale=False, xaxis=dict(tickangle=-20), height=400, **base_layout())
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Success Stories show the strongest positive sentiment (+0.31), while Side Effects & Questions posts trend negative — validating that the clustering captured meaningfully different patient experiences.")

    with col2:
        st.subheader("Mental Health Mentions")
        mh_counts = df_ml["mental_health_flag"].value_counts().reset_index()
        mh_counts.columns = ["Flag", "Count"]
        mh_counts["Flag"] = mh_counts["Flag"].map({0: "No Mention", 1: "Mental Health Mention"})
        fig3 = px.pie(mh_counts, names="Flag", values="Count", hole=0.4,
                      color_discrete_sequence=["#4fc3f7", "#e74c3c"],
                      template="plotly_dark")
        fig3.update_traces(hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>")
        fig3.update_layout(**base_layout())
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("6.95% of posts contain mental health mentions (depression, anxiety, suicidal ideation). While a minority, these posts attract disproportionately higher comment counts — suggesting the community actively supports distressed members.")

# =====================
# PAGE: ABOUT
# =====================
elif page == "About":
    st.title("About This Project")

    st.markdown("""
    ### Project Overview
    This dashboard presents findings from a multi-source healthcare data analytics pipeline
    analyzing real-world isotretinoin (Accutane) treatment outcomes. It combines two independent
    data sources to provide a more complete picture than either source alone.

    ### Data Sources
    **FDA FAERS (Food and Drug Administration Adverse Event Reporting System)**
    - 5 quarters of data: 2025 Q1 through 2026 Q1
    - 4,061 unique isotretinoin adverse event reports
    - 9,096 individual reaction entries across 1,234 unique reaction terms

    **r/Accutane (Reddit)**
    - 5,005 posts collected via Arctic Shift archive
    - Patient-reported treatment experiences, side effects, and outcomes

    ### Methodology
    - NLP sentiment analysis using VADER (Valence Aware Dictionary and sEntiment Reasoner)
    - K-Means clustering (k=4) on TF-IDF vectorized post text
    - Logistic regression classifier for mental health mention detection
    - Latent Dirichlet Allocation (LDA) topic modeling (5 topics)

    ### Limitations
    - FAERS captures adverse events only — it is not representative of all isotretinoin users
    - Reddit data reflects self-selected patient voices and may not be representative
    - Sentiment analysis was performed on informal text and may misclassify nuanced posts
    - Mental health prediction accuracy is 65% — sufficient for pattern detection, not clinical use
    - Small sample sizes for treatment months beyond month 6 limit reliability of month-level trends

    ### Disclaimer
    """)

    st.markdown('<div class="disclaimer">⚠️ This project is for academic research and portfolio purposes only. It does not constitute medical advice, clinical guidance, or endorsement of any treatment. All findings should be interpreted in the context of their data limitations. Consult a licensed dermatologist or physician before making any treatment decisions.</div>', unsafe_allow_html=True)

    st.markdown("""
    ### Built With
    PostgreSQL · Python · pandas · VADER · scikit-learn · Streamlit · Plotly · Arctic Shift · FDA FAERS
    """)