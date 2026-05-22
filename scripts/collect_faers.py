import pandas as pd
import os

base_path = r"C:\Users\16315\Desktop\Python\Projects\Accutane Database\faers_raw"
processed_path = r"C:\Users\16315\Desktop\Python\Projects\Accutane Database\processed"

quarters = [
    ("faers_ascii_2025q1", "25Q1"),
    ("faers_ascii_2025q2", "25Q2"),
    ("faers_ascii_2025q3", "25Q3"),
    ("faers_ascii_2025q4", "25Q4"),
    ("faers_ascii_2026q1", "26Q1"),
]

# Load the isotretinoin primaryids we already found
df_drug = pd.read_csv(os.path.join(processed_path, "drug_isotretinoin.csv"))
valid_ids = set(df_drug["primaryid"].unique())
print(f"Filtering by {len(valid_ids)} unique isotretinoin report IDs")

# Tables to collect
tables = ["REAC", "DEMO", "OUTC"]
results = {t: [] for t in tables}

for folder, q in quarters:
    print(f"\nProcessing {folder}...")
    for table in tables:
        path = os.path.join(base_path, folder, "ASCII", f"{table}{q}.txt")
        df = pd.read_csv(path, sep="$", encoding="latin-1", low_memory=False)
        df_filtered = df[df["primaryid"].isin(valid_ids)].copy()
        df_filtered["quarter"] = folder
        results[table].append(df_filtered)
        print(f"  {table}: {len(df_filtered)} rows")

# Save each table
for table in tables:
    df_combined = pd.concat(results[table], ignore_index=True)
    out_path = os.path.join(processed_path, f"{table.lower()}_isotretinoin.csv")
    df_combined.to_csv(out_path, index=False)
    print(f"\nSaved {table}: {len(df_combined)} rows → {out_path}")