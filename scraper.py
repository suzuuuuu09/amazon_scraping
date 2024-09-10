from time import sleep
from writer import CSV
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

class ProductScraper:
    def __init__(self, filename='product_info.csv'):
        self.filename = filename
        self.driver = self.setup_driver()
        self.csv_writer = CSV(self.filename)
        
        # 既存のCSVファイルがあれば削除する
        if os.path.exists(self.filename):
            os.remove(self.filename)
    
    def setup_driver(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # ブラウザを非表示にする
        chrome_options.add_argument("--ignore-certificate-errors")  # 証明書エラーを無視する
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    def open_new_tab(self, url):
        self.driver.execute_script(f"window.open('{url}', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])  # 最後のタブに切り替え
    
    def close_current_tab(self):
        self.driver.close()  # 現在のタブを閉じる
        self.driver.switch_to.window(self.driver.window_handles[-1])  # 最後のタブに切り替え
    
    def check_product_info(self):
        try:
            product_name = self.driver.find_element(By.ID, "productTitle").text
            price = self.driver.find_element(By.CLASS_NAME, "a-price-whole").text
            evaluations = self.driver.find_elements(By.CLASS_NAME, "a-size-base.a-color-base")
            evaluation = evaluations[1].text if len(evaluations) >= 2 else "評価情報が見つかりません"
            review = self.driver.find_element(By.ID, "acrCustomerReviewText").text.replace("個の評価", "")
            description = self.driver.find_element(By.ID, "feature-bullets").text.replace("› もっと見る", "")
            
            current_url = self.driver.current_url
            product_id = current_url.replace("https://www.amazon.co.jp/gp/product/", "")[:10]
            self.driver.get(f"https://sakura-checker.jp/itemsearch/?word={product_id}")
            sakura_evaluation = self.driver.find_element(By.CLASS_NAME, "item-rating").text.replace("/5", "")
            
            header = ["商品名", "価格", "評価", "評価数", "サクラ評価", "商品説明"]
            data = [product_name, price, evaluation, review, sakura_evaluation, description]
            self.csv_writer.write_data(header, data)
        
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    
    def scrape(self, search_url):
        self.driver.get(search_url)
        url_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".button.is-primary.is-small")
        urls = [button.get_attribute("href") for button in url_buttons if button.get_attribute("href")]
        
        for url in urls:
            self.open_new_tab(url)
            sleep(1)
            self.check_product_info()
            self.close_current_tab()  # タブを閉じる
    
    def quit(self):
        self.driver.quit()
