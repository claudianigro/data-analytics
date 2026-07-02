import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

df = pd.read_csv("products_asos.csv", on_bad_lines='skip')
df['price'] = pd.to_numeric(df['price'], errors = 'coerce')
df = df.dropna(subset = ['price'])
print(f"Data Loaded: {len(df)} rows")

df["description"] = df['description'].astype(str)
def get_brand(text):
    if "by" in text:
        try:
            return text.split('by ')[1].split(' ')[0]
        except:
            return "Unknown"
    return "Unknown"

df['brand_raw'] = df['description'].apply(get_brand)


brand_counts = df['brand_raw'].value_counts()
valid_brands = brand_counts[brand_counts>5].index
df_clean = df[df["brand_raw"].isin(valid_brands)].copy()