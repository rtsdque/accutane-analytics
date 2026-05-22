# Add to a quick script or run interactively
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/accutane_db")
df = pd.read_csv(r"C:\Users\16315\Desktop\Python\Projects\Accutane Database\processed\reddit_ml.csv")
df.to_sql("reddit_ml", engine, if_exists="replace", index=False)
print(f"Loaded {len(df)} rows into reddit_ml")