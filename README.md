# PTT 股票版爬蟲：川普新聞自動蒐集系統

這是一個透過 Windows 工作排程器執行的自動化爬蟲專案，會從 PTT 股票版中自動抓取最近 5 頁的文章，並找出標題包含「川普」的貼文。

蒐集到的文章標題及連結會：
- 寫入 MS SQL資料庫
- 發送至指定的 Discord 頻道
- 每次執行會記錄執行時間（log.txt）

## 執行結果示意

Discord 通知畫面截圖：
![Discord通知畫面](img/dc.png)

## 使用套件版本
- pyodbc==5.2.0
- python-dotenv==1.1.0
- requests==2.28.1
- beautifulsoup4==4.13.3
- lxml==5.0.0

## 檔案說明

- `crawler.py`：主爬蟲程式，從 PTT 股票版抓取包含「川普」的文章
- `db.py`：資料庫連線與寫入函式
- `dc_notifier.py`：發送 Discord 通知
- `clear_db.py`：清空資料表
- `show_db.py`：列出資料表內容
- `run_crawler.bat`：執行爬蟲的批次檔，可配合排程器使用
- `requirements.txt`：套件依賴清單