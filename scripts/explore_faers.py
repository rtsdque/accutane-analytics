import pandas as pd
import os

base_path = r"C:\Users\16315\Desktop\Python\Projects\Accutane Database\faers_raw"

quarters = [
    ("faers_ascii_2025q1", "DRUG25Q1.txt"),
    ("faers_ascii_2025q2", "DRUG25Q2.txt"),
    ("faers_ascii_2025q3", "DRUG25Q3.txt"),
    ("faers_ascii_2025q4", "DRUG25Q4.txt"),
    ("faers_ascii_2026q1", "DRUG26Q1.txt"),
]

search_terms = ["isotretinoin", "accutane", "claravis", "absorica", "amnesteem", "sotret", "myorisan"]

all_quarters = []

for folder, filename in quarters:
    path = os.path.join(base_path, folder, "ASCII", filename)
    df = pd.read_csv(path, sep="$", encoding="latin-1", low_memory=False)
    mask = df["drugname"].str.lower().str.contains("|".join(search_terms), na=False)
    df_filtered = df[mask].copy()
    df_filtered["quarter"] = folder  # tag which quarter it came from
    all_quarters.append(df_filtered)
    print(f"{folder}: {len(df_filtered)} isotretinoin rows")

df_all = pd.concat(all_quarters, ignore_index=True)
print(f"\nTotal across all quarters: {len(df_all)}")

output_path = os.path.join(base_path, "..", "processed", "drug_isotretinoin.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_all.to_csv(output_path, index=False)
print(f"\nSaved to {output_path}")