from scraper import ProductScraper

words = [
    "スマートウォッチ",
    "モバイルバッテリー",
    "マウス",
    "シェーバー",
    "ゲーム周辺機器",
    "折りたたみ傘",
    "懐中電灯",
    "ランタン",
    "害獣・害虫対策器",
    "椅子",
    "ヘアドライヤー",
    "アイマッサージャー",
    "美顔器・美容器",
    "加湿器",
    "EMS・腹筋ベルト",
    "枕",
    "タオル",
    "寝具カバー・シーツ"
]

scraper = ProductScraper()
for word in words:
    for i in range(3):
        scraper.scrape(f"https://sakura-checker.jp/itemsearch/?page={i + 1}&sort=amazon&word={word}")
scraper.quit()
