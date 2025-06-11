import requests
from bs4 import BeautifulSoup
import re
from db import insert_news
# PTT 股票版爬蟲
# 目標：抓取最新5頁中包含「川普」的文章，並寫入資料庫
def get_latest_page():
    url = "https://www.ptt.cc/bbs/Stock/index.html"
    resp = requests.get(url)
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

latest = get_latest_page()
if not latest:
    print("找不到最新頁碼！")
else:
    for page_num in range(latest, latest - 5, -1):  # 抓最新前5頁
        url = f"https://www.ptt.cc/bbs/Stock/index{page_num}.html"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        for entry in soup.select(".r-ent"):
            title_tag = entry.select_one(".title a")
            if title_tag:
                title = title_tag.text.strip()
                if "川普" in title:
                    link = "https://www.ptt.cc" + title_tag["href"]
                    author = entry.select_one(".author").text.strip()
                    date = entry.select_one(".date").text.strip()
                    insert_news(date, title, link, "")  # 這裡的 content 留空，因為 PTT 的文章內容需要進一步抓取