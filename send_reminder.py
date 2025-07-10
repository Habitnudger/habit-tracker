from dotenv import load_dotenv
import os, requests
from datetime import datetime

load_dotenv()
token   = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")

text = f"💡 Habit check-in — {datetime.now():%H:%M}\nTap ✅ when you’ve done it!"

requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage",
    json={
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {
            "inline_keyboard": [[
                {"text": "✅ Done", "callback_data": "done"}
            ]]
        }
    }
)
print("Reminder sent ✔")
