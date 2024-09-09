from writer import CSV
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# urls = {
#     'https://amzn.asia/d/ciyByNY',
#     'https://amzn.asia/d/4sX4XNg',
#     'https://amzn.asia/d/h1t8Vp9'
# }
# filename = 'product_info.csv'

# for url in urls:
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")     # ブラウザを表示しない
#     chrome_options.add_argument("--ignore-certificate-errors")  # 証明書エラーを無視する

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#     driver.get(url)

#     try:
#         product_name = driver.find_element(By.ID, "productTitle").text
#         price = driver.find_element(By.CLASS_NAME, "a-price-whole").text
#         evaluations = driver.find_elements(By.CLASS_NAME, "a-size-base.a-color-base")
#         if len(evaluations) >= 2:
#             evaluation = evaluations[1].text  # 2番目の要素を取得
#         else:
#             evaluation = "評価情報が見つかりません"
#         review = driver.find_element(By.ID, "acrCustomerReviewText").text.replace("個の評価", "")
#         description = driver.find_element(By.ID, "feature-bullets").text.replace("› もっと見る", "")

#         header = ["商品名", "価格", "評価", "評価数", "商品説明"]
#         data = [product_name, price, evaluation, review, description]

#         csv_writer = CSV(filename)
#         csv_writer.write_data(header, data)
    
#     except Exception as e:
#         print(f"エラーが発生しました: {e}")

#     finally:
#         driver.quit()

url="https://amzn.asia/d/ciyByNY"
chrome_options = Options()
# chrome_options.add_argument("--headless")     # ブラウザを表示しない
chrome_options.add_argument("--ignore-certificate-errors")  # 証明書エラーを無視する

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(url)

current_url = driver.current_url
product_id = current_url.replace("https://www.amazon.co.jp/dp/", "")[:10]
driver.get(f"https://sakura-checker.jp/itemsearch/?word={product_id}")
rating = driver.find_element(By.CLASS_NAME, "item-rating").text.replace("/5", "")
print(rating)

driver.quit()