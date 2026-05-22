import pandas as pd
from sqlalchemy import create_engine
import os

# Database connection
engine = create_engine("postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/accutane_db")

processed_path = r"C:\Users\16315\Desktop\Python\Projects\Accutane Database\processed"

# Define CSVs and their target table names
files = {
    "drug_isotretinoin.csv": "faers_drug",
    "reac_isotretinoin.csv": "faers_reac",
    "demo_isotretinoin.csv": "faers_demo",
    "outc_isotretinoin.csv": "faers_outc",
    "reddit_accutane.csv": "reddit_posts"
}

for filename, table_name in files.items():
    path = os.path.join(processed_path, filename)
    df = pd.read_csv(path, low_memory=False)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into {table_name}")

print("\nAll tables loaded successfully.")