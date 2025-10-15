#!/usr/bin/env bash
# =========================================
#  Shock Dashboard Starter (macOS)
#  Startet das Dashboard, öffnet README + Dashboard
#  und schließt sich nach Bestätigung automatisch.
# =========================================

set -euo pipefail

# --- Projektpfad anpassen ---
cd "$HOME/Dokumente/shock_dashboard" || { echo "❌ Projektordner nicht gefunden."; exit 1; }

# --- Gatekeeper-Beschränkung entfernen ---
xattr -d com.apple.quarantine "$0" >/dev/null 2>&1 || true

# --- Logs & Output-Ordner ---
mkdir -p out logs

# --- Virtuelle Umgebung vorbereiten ---
if [ -d ".venv" ]; then
  source .venv/bin/activate
else
  /usr/bin/python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install requests yfinance python-dotenv pyyaml
fi

# --- Zeitzone setzen ---
export TZ="Europe/Berlin"

echo "🚀 Starte Shock Dashboard..."
echo

# --- Dashboard ausführen ---
python3 shock_dashboard.py --use-fred --use-yf --out out/ | tee -a "logs/manual_run.log"

echo
echo "✅ Dashboard fertig erstellt!"
echo "📂 Dateien gespeichert unter: out/shock_dashboard.md & out/shock_dashboard.json"
echo

# --- Dashboard + README öffnen ---
open out/shock_dashboard.md
open README.md || true

echo
read -p "🧭 Prozess abgeschlossen. Drücke [Enter], um alles zu schließen... " _

# --- Terminal schließen ---
osascript -e 'tell application "Terminal" to close (every window whose name contains "Start_Dashboard.command")' &> /dev/null &
exit 0
