import pandas as pd

df = pd.read_csv("data/product_info.csv")

df['価格'] = df['価格'].str.replace('"', '').str.replace(',', '')
df['評価数'] = df['評価数'].str.replace('"', '').str.replace(',', '')

df.to_csv("data/processed_product_info.csv", index=False)