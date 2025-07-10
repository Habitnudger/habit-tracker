from dotenv import load_dotenv
import os, requests
from datetime import datetime

load_dotenv()                       # reads TELEGRAM_TOKEN & CHAT_ID
token   = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")

text = f"✅ Habit-tracker test — {datetime.now():%H:%M}"

requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage",
    json={"chat_id": chat_id, "text": text}
)
print("Message sent ✔")

