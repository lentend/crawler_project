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
    title NVARCHAR(255),
    url NVARCHAR(500),
    content NVARCHAR(MAX)
)
""")
conn.commit()

# 寫入資料函式
def insert_news(title, url, content):
    cursor.execute(
        "INSERT INTO news (title, url, content) VALUES (?, ?, ?)",
        (title, url, content)
    )
    conn.commit()

# 測試寫入
if __name__ == "__main__":
    insert_news("測試標題", "https://example.com", "這是一筆測試資料")
    print("資料寫入成功")
