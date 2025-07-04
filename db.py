import pyodbc
import os
from dotenv import load_dotenv
load_dotenv()  # 載入 .env 中的變數

# 連線設定（密碼請改為你設定的密碼）
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
)
cursor = conn.cursor()

# 建立資料表（只會建立一次）
cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='news' AND xtype='U')
CREATE TABLE news (
    id INT IDENTITY(1,1) PRIMARY KEY,
    date NVARCHAR(20),
    title NVARCHAR(255),
    url NVARCHAR(500),
    content NVARCHAR(MAX)
)
""")
conn.commit()

# 寫入資料函式
def insert_news(date, title, url, content):
    try:
        cursor.execute(
            "INSERT INTO news (date, title, url, content) VALUES (?, ?, ?, ?)",
            (date, title, url, content)
        )
        conn.commit()
        print(f"已寫入：{title} | {url}")
        return True  #  表示成功寫入
    except Exception as e:
        # 捕捉 UNIQUE 約束違反（網址重複）時自動略過
        if "UNIQUE" in str(e) or "unique" in str(e):
            print(f"已存在（網址重複，略過）：{url}")
        else:
            print(f"寫入失敗：{title}，錯誤訊息：{e}")

# 顯示所有新聞資料
def show_all_news():
    cursor.execute("SELECT * FROM news")
    for row in cursor.fetchall():
        print(row)

# 清空資料表
def clear_news_table():
    cursor.execute("DELETE FROM news")
    cursor.execute("DBCC CHECKIDENT ('news', RESEED, 0)")
    conn.commit()
    print("news 資料表已清空且自動編號已重設")

#更新
def update_news_date(news_id, new_date):
    cursor.execute("""
    UPDATE news
    SET date = ?
    WHERE id = ?
    """, (new_date, news_id))
    conn.commit()
    print(f"已更新 ID {news_id} 的日期為 {new_date}")

# 手動更新日期
def manual_update_date():
    try:
        news_id = int(input("請輸入要更新的新聞 ID："))
        new_date = input("請輸入新的日期（例如 2025-06-20）：")
        update_news_date(news_id, new_date)
    except Exception as e:
        print(f"更新失敗：{e}")



# 測試寫入
if __name__ == "__main__":
    manual_update_date()
