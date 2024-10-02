import pandas as pd

df = pd.read_csv("data/product_info.csv")

df['商品説明'] = df['商品説明'].str.strip()
df['価格'] = df['価格'].str.replace('"', '').str.replace(',', '')
df['評価数'] = df['評価数'].str.replace('"', '').str.replace(',', '')

# print(df['商品説明'].isnull())
df = df.dropna(subset=['商品説明'])

with open("output.txt", "r") as f:
    seikakudo_data = f.read().split("\n")

df['商品説明正確度'] = seikakudo_data

df.to_csv("data/processed_product_info.csv", index=False)