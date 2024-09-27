from time import sleep
from writer import CSV
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class ProductScraper:
    def __init__(self, filename='product_info.csv'):
        self.filename = filename
        self.driver = self.setup_driver()
        self.csv_writer = CSV(self.filename)
        
        if os.path.exists(self.filename):
            os.remove(self.filename)  # 既存のCSVファイルがあれば削除する
    
    def setup_driver(self):
        CHROME_OPTIONS = Options()
        # CHROME_OPTIONS.add_argument("--headless")  # ブラウザを非表示にする
        CHROME_OPTIONS.add_argument("--ignore-certificate-errors")  # 証明書エラーを無視する
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=CHROME_OPTIONS)
    
    def open_new_tab(self, url):
        self.driver.execute_script(f"window.open('{url}', '_blank');")  # 新しいタブで開く
        self.driver.switch_to.window(self.driver.window_handles[-1])  # 最後のタブに切り替え
    
    def close_current_tab(self):
        self.driver.close()  # 現在のタブを閉じる
        self.driver.switch_to.window(self.driver.window_handles[-1])  # 最後のタブに切り替え
    
    def check_product_info(self):
        try:
            # 商品名が表示されるまで待機
            product_name = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "productTitle"))
            ).text  # 商品名

            # 価格が表示されるまで待機
            price = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a-price-whole"))
            ).text  # 価格
            
            evaluations = self.driver.find_elements(By.CLASS_NAME, "a-size-base.a-color-base")
            evaluation = evaluations[1].text if len(evaluations) > 1 else 0
            
            # 評価数が表示されるまで待機
            review = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "acrCustomerReviewText"))
            ).text.replace("個の評価", "")  # 評価数
            
            # 商品説明が表示されるまで待機
            description = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "feature-bullets"))
            ).text.replace("› もっと見る", "").replace("この商品について", "")  # 商品説明
            
            # 企業名が表示されるまで待機
            company = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "bylineInfo"))
            ).text.replace("のストアを表示", "")  # 企業名

            current_url = self.driver.current_url  # 現在のURLを取得
            product_id = current_url.replace("https://www.amazon.co.jp/gp/product/", "")[:10]  # 商品ID
            self.driver.get(f"https://sakura-checker.jp/itemsearch/?word={product_id}")  # サクラチェッカーを開く
            
            # サクラチェッカー内の評価が表示されるまで待機
            sakura_evaluation = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "item-rating"))
            ).text.replace("/5", "")  # サクラ評価

            header = ["商品名", "企業名", "価格", "評価", "評価数", "サクラ評価", "商品説明"]
            data = [product_name, company, price, evaluation, review, sakura_evaluation, description]
            self.csv_writer.write_data(header, data)
            print(company)
        
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    
    def scrape(self, search_url):
        self.driver.get(search_url)  # serach_urlのリンクに飛ぶ
        url_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".button.is-primary.is-small")  # 商品の詳細ボタンを取得する
        urls = [button.get_attribute("href") for button in url_buttons if button.get_attribute("href")]  # 詳細ボタンのURLを取得する
        
        for url in urls:
            self.open_new_tab(url)  # 新しいタブでURLを開く
            sleep(1)
            self.check_product_info()  # 商品情報のチェックする
            self.close_current_tab()  # タブを閉じる
    
    def quit(self):
        self.driver.quit()
