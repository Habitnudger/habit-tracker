import os, csv, requests
from datetime import datetime, timezone, timedelta
from collections import Counter, OrderedDict

TOKEN   = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CSV     = "log.csv"

# ---------- load this week’s rows ----------
start_of_week = (datetime.now(timezone.utc)
                 .astimezone(timezone.utc)
                 .replace(hour=0, minute=0, second=0, microsecond=0)
                 - timedelta(days=datetime.now().weekday()))  # Monday 00:00 UTC
counts = Counter()

with open(CSV) as f:
    for row in csv.reader(f):
        if row[0] == "datetime":           # skip header
            continue
        t = datetime.fromisoformat(row[0])
        if t >= start_of_week:
            counts[t.strftime("%a")] += 1  # Mon, Tue, …

# ensure all 7 days are present in order
days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
ordered = OrderedDict((d, counts.get(d, 0)) for d in days)

# ---------- build text ----------
total = sum(ordered.values())
possible = 5 * len([d for d in days if datetime.now().strftime("%a") >= d])  # 5 prompts/day
pct = round(100 * total / possible) if possible else 0

lines = [f"📊 *Weekly Habit Report*",
         f"Period: {start_of_week:%d %b} – {(start_of_week+timedelta(days=6)):%d %b}",
         "",
         "\n".join(f"{d}: {ordered[d]}" for d in days),
         "",
         f"✅ {total} / {possible} = *{pct} %*"]
text = "\n".join(lines)

# ---------- send to Telegram ----------
requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
)
print("Summary sent ✔")
