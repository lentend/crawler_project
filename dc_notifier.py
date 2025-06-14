import requests
import os
from dotenv import load_dotenv
load_dotenv()

def send_to_discord(title, link):
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    content = f"[{title}]({link})"
    data = {"content": content}
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"Discord 發送失敗：{response.status_code} - {response.text}")
    else:
        print(f"Discord 發送成功：{title} | {link}")
