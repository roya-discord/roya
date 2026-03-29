import os
import requests
import time

BLOXFLIP_TOKEN = os.environ["BLOXFLIP_TOKEN"]
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]
POLL_INTERVAL = 15

HEADERS = {
    "x-auth-token": BLOXFLIP_TOKEN,
    "Content-Type": "application/json"
}

def get_transactions():
    r = requests.get("https://api.bloxflip.com/user/transactions", headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    return None

def send_discord_alert(tip):
    payload = {
        "content": "<@1359507148794495006>",
        "embeds": [{
            "title": "💰 New Tip/Gift Received!",
            "color": 0x00ff99,
            "fields": [
                {"name": "From", "value": str(tip.get("from", "Unknown")), "inline": True},
                {"name": "Amount", "value": str(tip.get("amount", "?")), "inline": True},
                {"name": "Time", "value": str(tip.get("createdAt", "?")), "inline": False},
            ]
        }]
    }
    requests.post(DISCORD_WEBHOOK, json=payload)

seen_ids = set()
print("Watching for tips...")
while True:
    data = get_transactions()
    if data:
        for tx in data.get("transactions", []):
            if tx.get("type") == "tip" and tx["_id"] not in seen_ids:
                seen_ids.add(tx["_id"])
                send_discord_alert(tx)
                print(f"New tip detected: {tx}")
    time.sleep(POLL_INTERVAL)
