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

def calculate_phantom_revenue(size_str):
    if not isinstance(size_str, str):
        return 0, 0.0
    sizes =size_str.split(',')
    total_sizes = len(sizes)

    out_of_stock_count = size_str.count("Out of stock")
    rate = out_of_stock_count/total_sizes if total_sizes > 0 else 0.0
    return out_of_stock_count,  rate

metrics = df_clean["size"].apply(lambda x: calculate_phantom_revenue(x))
df_clean['Stockout_Count'] = [x[0] for x in metrics]
df_clean["Stockout_Rate"] = [x[1] for x in metrics]

df_clean["Lost_Revenue"] = df_clean['price'] * df_clean['Stockout_Count']

cols = ["brand_raw", "name", "price", "Stockout_Count", "Lost_Revenue"]
print(df_clean.sort_values(by="Lost_Revenue", ascending = False).head(10)[cols])