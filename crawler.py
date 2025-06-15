import requests
from bs4 import BeautifulSoup
import re
from db import insert_news
from datetime import datetime
from dc_notifier import send_to_discord
import time
from concurrent.futures import ThreadPoolExecutor

start_time = time.time()
# PTT 股票版爬蟲
# 目標：抓取最新5頁中包含「川普」的文章，並寫入資料庫

session = requests.Session() # 重複利用連線

with open("log.txt", "a", encoding="utf-8") as f:
    f.write(f"爬蟲執行時間：{datetime.now()}\n")

# === 取得最新頁碼 ===    
def get_latest_page():
    url = "https://www.ptt.cc/bbs/Stock/index.html"
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    prev_link = None
    # 遍歷所有分頁按鈕，找到「上頁」
    for btn in soup.select('div.btn-group-paging a'):
        if "上頁" in btn.text:
            prev_link = btn
            break
    if prev_link:
        match = re.search(r'index(\d+)\.html', prev_link['href'])
        if match:
            # 最新頁 = 「上一頁頁碼」+1
            return int(match.group(1)) + 1
    return None

# 使用多線程加速爬取
def process_page(page_num):
    url = f"https://www.ptt.cc/bbs/Stock/index{page_num}.html"
    try:
        resp = session.get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        for entry in soup.select(".r-ent"):
            title_tag = entry.select_one(".title a")
            if title_tag:
                title = title_tag.text.strip()
                if "川普" in title:
                    link = "https://www.ptt.cc" + title_tag["href"]
                    author = entry.select_one(".author").text.strip()
                    date = entry.select_one(".date").text.strip()
                    if insert_news(date, title, link, ""):
                        send_to_discord(title, link)
    except Exception as e:
        print(f"第 {page_num} 頁失敗：{e}")

# === 主程式 ===
latest = get_latest_page()
if not latest:
    print("找不到最新頁碼！")
else:
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_page, range(latest, latest - 5, -1))

elapsed = time.time() - start_time
print(f"爬蟲完成，總耗時：{elapsed:.2f} 秒")