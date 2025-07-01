import requests
import os
from dotenv import load_dotenv
load_dotenv()

def send_to_discord(title, link, content):
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    preview = content.strip().replace("\n", " ").replace("\r", "")[:300]

    # 組合訊息內容：標題連結 + 內文 preview 包在 code block 裡
    message = f"[{title}]({link})\n```\n{preview}\n```"

    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"Discord 發送失敗：{response.status_code} - {response.text}")
    else:
        print(f"Discord 發送成功：{title} | {link}")
