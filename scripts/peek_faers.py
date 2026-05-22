import pandas as pd
import os

processed_path = r"C:\Users\16315\Desktop\Python\Projects\Accutane Database\processed"

# Peek at REAC
df_reac = pd.read_csv(os.path.join(processed_path, "reac_isotretinoin.csv"))
print("=== REAC (Reactions) ===")
print(df_reac.columns.tolist())
print(df_reac.head(10))
print(f"\nUnique reaction terms: {df_reac['pt'].nunique()}")
print(f"\nTop 20 most reported reactions:")
print(df_reac['pt'].value_counts().head(20))

print("\n")

# Peek at DEMO
df_demo = pd.read_csv(os.path.join(processed_path, "demo_isotretinoin.csv"))
print("=== DEMO (Demographics) ===")
print(df_demo.columns.tolist())
print(df_demo.head(10))
print(f"\nSex breakdown:")
print(df_demo['sex'].value_counts())
print(f"\nAge stats:")
print(df_demo['age'].describe())