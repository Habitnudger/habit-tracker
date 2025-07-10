import os, csv, requests, subprocess, json
from datetime import datetime, timezone

TOKEN        = os.getenv("TELEGRAM_TOKEN")
CHAT_ID      = os.getenv("CHAT_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
LOG_PATH     = "log.csv"
OFFSET_FILE  = ".last_update_id"

# read last processed Telegram update ID
offset = 0
if os.path.exists(OFFSET_FILE):
    with open(OFFSET_FILE) as f:
        offset = int(f.read().strip())

resp = requests.get(
    f"https://api.telegram.org/bot{TOKEN}/getUpdates",
    params={"offset": offset + 1, "timeout": 0}
).json()
updates = resp.get("result", [])

new_offset = offset
rows_to_add = []

for u in updates:
    new_offset = max(new_offset, u["update_id"])
    if u.get("callback_query", {}).get("data") == "done":
        when = datetime.now(timezone.utc).isoformat(timespec="seconds")
        rows_to_add.append([when])

# save new offset
with open(OFFSET_FILE, "w") as f:
    f.write(str(new_offset))

# append new rows to CSV
if rows_to_add:
    with open(LOG_PATH, "a", newline="") as f:
        csv.writer(f).writerows(rows_to_add)

# commit & push if anything changed
if rows_to_add:
    subprocess.run(["git", "config", "--global", "user.email", "bot@github"], check=True)
    subprocess.run(["git", "config", "--global", "user.name",  "GitHub Actions"], check=True)
    subprocess.run(["git", "add", LOG_PATH, OFFSET_FILE], check=True)
    subprocess.run(["git", "commit", "-m", f"Add {len(rows_to_add)} check-ins"], check=True)
    subprocess.run(["git", "push", "origin", "HEAD"], check=True)   # simple & safe
