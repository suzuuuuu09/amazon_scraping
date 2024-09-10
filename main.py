from scraper import ProductScraper

scraper = ProductScraper()
for i in range(1, 4):
    scraper.scrape(f"https://sakura-checker.jp/itemsearch/?page={i}&sort=amazon&word=イヤホン")
scraper.quit()
