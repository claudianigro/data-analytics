import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

df = pd.read_csv("products_asos.csv", on_bad_lines='skip')
df['price'] = pd.to_numeric(df['price'], errors = 'coerce')
df = df.dropna(subset = ['price'])
print(f"Data Loaded: {len(df)} rows")