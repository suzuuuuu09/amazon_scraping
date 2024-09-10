from time import sleep
from writer import CSV
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os

# urls = {
#     'https://amzn.asia/d/ciyByNY',
#     'https://amzn.asia/d/4sX4XNg',
#     'https://amzn.asia/d/h1t8Vp9',
#     "https://amzn.asia/d/8TAHnJx"
# }
filename = 'product_info.csv'

if os.path.exists(filename):
  os.remove(filename)     # CSVファイルの削除をする

chrome_options = Options()
    # chrome_options.add_argument("--headless")     # ブラウザを表示しない
chrome_options.add_argument("--ignore-certificate-errors")  # 証明書エラーを無視する
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def open_new_tab(url):
    driver.execute_script(f"window.open('{url}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])  # 最後に追加されたタブに切り替える

def check_product_info():
    try:
        product_name = driver.find_element(By.ID, "productTitle").text
        price = driver.find_element(By.CLASS_NAME, "a-price-whole").text
        evaluations = driver.find_elements(By.CLASS_NAME, "a-size-base.a-color-base")
        if len(evaluations) >= 2:
            evaluation = evaluations[1].text  # 2番目の要素を取得
        else:
            evaluation = "評価情報が見つかりません"
        review = driver.find_element(By.ID, "acrCustomerReviewText").text.replace("個の評価", "")
        description = driver.find_element(By.ID, "feature-bullets").text.replace("› もっと見る", "")

        current_url = driver.current_url    # 現在のURLを取得する
        product_id = current_url.replace("https://www.amazon.co.jp/gp/product/", "")[:10]     # 製品IDを取得する
        driver.get(f"https://sakura-checker.jp/itemsearch/?word={product_id}")     # サクラチェッカーで検索する
        sakura_evaluation = driver.find_element(By.CLASS_NAME, "item-rating").text.replace("/5", "")     # サクラチェッカーの評価を取得する

        header = ["商品名", "価格", "評価", "評価数", "サクラ評価", "商品説明"]
        data = [product_name, price, evaluation, review, sakura_evaluation, description]

        csv_writer = CSV(filename)
        csv_writer.write_data(header, data)
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")

driver.get("https://sakura-checker.jp/itemsearch/?sort=amazon&word=イヤホン")

url_buttons = driver.find_elements(By.CSS_SELECTOR, ".button.is-primary.is-small")

urls = [button.get_attribute("href") for button in url_buttons if button.get_attribute("href")]

for url in urls:
    open_new_tab(url)
    sleep(1)
    check_product_info()

# for url in urls:

# driver.quit()
    
