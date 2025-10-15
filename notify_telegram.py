from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

import os, json, pathlib, requests, sys

TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    sys.exit("❌ TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID fehlen (.env prüfen)")

p = pathlib.Path("out/shock_dashboard.json")
if not p.exists():
    sys.exit("❌ out/shock_dashboard.json nicht gefunden – erst Dashboard laufen lassen.")

d = json.load(open(p, "r", encoding="utf-8"))
score = d.get("total_score", 0)

emoji = {"green":"🟢","yellow":"🟡","orange":"🟠","red":"🔴"}
lines = [
    "📊 Shock Dashboard Update",
    f"Score: {score:.2f}/100",
    ""
]
for i in d.get("indicators", []):
    lines.append(f"{emoji.get(i.get('status','').lower(),'⚪️')} {i.get('name','')}: {i.get('value','')} {i.get('unit','')}")

msg = "\n".join(lines)

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
resp = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
try:
    resp.raise_for_status()
    print("✅ Telegram-Nachricht gesendet.")
except Exception as e:
    print("❌ Telegram-Fehler:", resp.text)
    sys.exit(1)
