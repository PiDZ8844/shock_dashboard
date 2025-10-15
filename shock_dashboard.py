#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Shock Dashboard (9 Indikatoren) – robust & deutsch
- FRED (FRED_API_KEY aus Umgebung), Yahoo Finance (ohne Key)
- Europe/Berlin Zeitzone
- 2 Nachkommastellen Anzeige, "error" bei fehlenden Werten
- Emoji-Farben: 🟢🟡🟠🔴 (⚪️ = unbekannt/Fehler)
- ShockScore 0..100 (0 = gut, 100 = maximaler Stress)
- Output: out/shock_dashboard.md & out/shock_dashboard.json
"""

import os
import json
import math
import argparse
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from zoneinfo import ZoneInfo

# optionale Abhängigkeiten
try:
    import requests
except Exception:
    requests = None

try:
    import yfinance as yf
except Exception:
    yf = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# ----------------- Hilfsfunktionen -----------------

def r2(x: Any) -> Any:
    """Rundet Zahlen auf 2 Nachkommastellen. Strings (inkl. 'error') bleiben erhalten."""
    try:
        if x is None:
            return None
        if isinstance(x, str):
            return x
        return round(float(x), 2)
    except Exception:
        return x

def fmt2(x: Any, unit: str = "") -> str:
    """Formatiert für Anzeige; 'error' bleibt 'error'."""
    if x is None:
        return "-"
    if isinstance(x, str) and x.strip().lower() == "error":
        return "error"
    try:
        return f"{float(x):.2f}{unit}"
    except Exception:
        return str(x)

def status_emoji(status: str) -> str:
    return {
        "green": "🟢",
        "yellow": "🟡",
        "orange": "🟠",
        "red": "🔴",
        "gray": "⚪️",
    }.get(status, "⚪️")

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

# ----------------- Fetcher -----------------

def fetch_fred_latest(series_id: str, api_key: Optional[str]) -> Optional[float]:
    """Holt den letzten FRED-Wert als float (oder None)."""
    if requests is None or not api_key:
        return None
    try:
        url = (
            "https://api.stlouisfed.org/fred/series/observations"
            f"?series_id={series_id}&api_key={api_key}&file_type=json&sort_order=desc&limit=1"
        )
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        obs = data.get("observations", [])
        if not obs:
            return None
        v = obs[0].get("value")
        if v in (None, ".", ""):
            return None
        return float(v)
    except Exception:
        return None

def fetch_yf_last(symbol: str) -> Optional[float]:
    """Holt den letzten Daily-Schlusskurs (robust über 5d Historie)."""
    if yf is None:
        return None
    try:
        hist = yf.Ticker(symbol).history(period="5d", interval="1d", auto_adjust=True)
        if hist is None or hist.empty:
            return None
        return float(hist["Close"].iloc[-1])
    except Exception:
        return None

def fetch_yf_ma(symbol: str, window: int) -> Optional[float]:
    """Einfache Gleitender Durchschnitt."""
    if yf is None:
        return None
    try:
        period = "500d" if window >= 200 else "200d"
        hist = yf.Ticker(symbol).history(period=period, interval="1d", auto_adjust=True)
        if hist is None or hist.empty:
            return None
        s = hist["Close"].dropna()
        if len(s) < window:
            return None
        return float(s.rolling(window).mean().iloc[-1])
    except Exception:
        return None

# ----------------- Schwellen & Klassifikation -----------------

DEFAULT_CFG: Dict[str, Dict[str, float]] = {
    "thresholds": {
        # 1) Yield Curve (10Y-2Y), höher ist besser
        "yc_10y2y": {"green": 0.30, "yellow": 0.00, "orange": -0.30},
        # 2) DXY, höher ist schlechter
        "dxy": {"green": 102.0, "yellow": 106.0, "orange": 110.0},
        # 3) UST10, höher ist schlechter
        "ust10": {"green": 3.50, "yellow": 4.50, "orange": 5.00},
        # 4) VIX, höher ist schlechter
        "vix": {"green": 20.0, "yellow": 25.0, "orange": 35.0},
        # 5) HY OAS (%), höher ist schlechter
        "hy_oas": {"green": 4.0, "yellow": 6.0, "orange": 8.0},
        # 6) Reverse Repo ($bn), niedriger ist schlechter (Interpretation tricky)
        "rrp": {"green": 100.0, "yellow": 10.0, "orange": 0.0},
        # 7) SPX MA50-MA200 (pts), höher ist besser (Death Cross < 0)
        "spx_ma": {"green": 0.0, "yellow": -50.0, "orange": -150.0},
        # 8) WTI, höher ist schlechter (Inflationsdruck)
        "wti": {"green": 60.0, "yellow": 100.0, "orange": 120.0},
        # 9) Gold, höher ist eher Risk-Off/Stress
        "gold": {"green": 2200.0, "yellow": 2800.0, "orange": 3200.0},
    }
}

def th(cfg: Dict[str, Any], name: str) -> Dict[str, float]:
    """Sicherer Zugriff auf thresholds, fällt auf Defaults zurück."""
    try:
        thresholds = (cfg or {}).get("thresholds", {}) or {}
        got = thresholds.get(name)
        if isinstance(got, dict):
            return got
        return DEFAULT_CFG["thresholds"][name]
    except Exception:
        return DEFAULT_CFG["thresholds"].get(name, {})

def classify(value: Any, limits: Dict[str, float], *, higher_is_worse: bool) -> str:
    """Mappt einen Wert auf Status. Nicht-numerisch → 'gray'."""
    try:
        v = float(value)
    except Exception:
        return "gray"

    g = limits.get("green")
    y = limits.get("yellow")
    o = limits.get("orange")

    if higher_is_worse:
        # kleiner besser
        if v < g:
            return "green"
        if v < y:
            return "yellow"
        if v < o:
            return "orange"
        return "red"
    else:
        # größer besser
        if v >= g:
            return "green"
        if v >= y:
            return "yellow"
        if v >= o:
            return "orange"
        return "red"

def status_to_score(status: str) -> float:
    """Status → 0..1 (0 gut, 1 schlecht)."""
    return {
        "green": 0.2,
        "yellow": 0.5,
        "orange": 0.8,
        "red": 1.0,
        "gray": 0.6,
    }.get(status, 0.6)

# ----------------- Datentyp -----------------

@dataclass
class Indicator:
    name: str
    value: Any
    unit: str
    comment: str
    status: str

# ----------------- Build Indikatoren -----------------

def build_indicators(use_fred: bool, use_yf: bool, cfg: Dict[str, Any]) -> List[Indicator]:
    fred_key = os.getenv("FRED_API_KEY")
    ind: List[Indicator] = []

    # 1) Yield Curve (10Y–2Y) – FRED T10Y2Y
    yc = fetch_fred_latest("T10Y2Y", fred_key) if use_fred else None
    yc_val = "error" if yc is None else r2(yc)
    yc_status = classify(yc_val, th(cfg, "yc_10y2y"), higher_is_worse=False)
    ind.append(Indicator("Yield Curve (10Y–2Y)", yc_val, "%", "Positive = normal, negative = inversion", yc_status))

    # 2) DXY – Yahoo
    dxy = fetch_yf_last("^DXY") if use_yf else None
    if dxy is None and use_yf:
        dxy = fetch_yf_last("DX-Y.NYB")
    dxy_val = "error" if dxy is None else r2(dxy)
    dxy_status = classify(dxy_val, th(cfg, "dxy"), higher_is_worse=True)
    ind.append(Indicator("US Dollar Index (DXY)", dxy_val, "", "Starker USD belastet Risikoassets", dxy_status))

    # 3) UST 10Y – FRED DGS10
    ust10 = fetch_fred_latest("DGS10", fred_key) if use_fred else None
    ust10_val = "error" if ust10 is None else r2(ust10)
    ust10_status = classify(ust10_val, th(cfg, "ust10"), higher_is_worse=True)
    ind.append(Indicator("UST 10Y Yield", ust10_val, "%", "Hohe Renditen drücken Bewertungen", ust10_status))

    # 4) VIX – Yahoo
    vix = fetch_yf_last("^VIX") if use_yf else None
    vix_val = "error" if vix is None else r2(vix)
    vix_status = classify(vix_val, th(cfg, "vix"), higher_is_worse=True)
    ind.append(Indicator("VIX (S&P 500 Volatility)", vix_val, "", "Angstbarometer", vix_status))

    # 5) HY OAS – FRED BAMLH0A0HYM2
    hy = fetch_fred_latest("BAMLH0A0HYM2", fred_key) if use_fred else None
    hy_val = "error" if hy is None else r2(hy)
    hy_status = classify(hy_val, th(cfg, "hy_oas"), higher_is_worse=True)
    ind.append(Indicator("US High Yield Spread", hy_val, "%", "Kreditstress", hy_status))

    # 6) Reverse Repo – FRED RRPONTSYD (Million → bn Heuristik)
    rrp = fetch_fred_latest("RRPONTSYD", fred_key) if use_fred else None
    if rrp is None:
        rrp_val = "error"
    else:
        rrp_val = r2(rrp / 1000.0 if rrp > 1000 else rrp)
    rrp_status = classify(rrp_val, th(cfg, "rrp"), higher_is_worse=False)
    ind.append(Indicator("Reverse Repo ($bn)", rrp_val, "bn", "Liquiditätsparkplatz; starker Rückgang = Abzug", rrp_status))

    # 7) SPX Struktur (MA50–MA200) – Yahoo
    ma50 = fetch_yf_ma("^GSPC", 50) if use_yf else None
    ma200 = fetch_yf_ma("^GSPC", 200) if use_yf else None
    if ma50 is None or ma200 is None:
        spx_diff = "error"
        spx_status = "gray"
    else:
        spx_diff = r2(ma50 - ma200)
        spx_status = classify(spx_diff, th(cfg, "spx_ma"), higher_is_worse=False)
    ind.append(Indicator("S&P 500 Structure (MA50 vs MA200)", spx_diff, "pts", "Death Cross < 0", spx_status))

    # 8) WTI – Yahoo
    wti = fetch_yf_last("CL=F") if use_yf else None
    wti_val = "error" if wti is None else r2(wti)
    wti_status = classify(wti_val, th(cfg, "wti"), higher_is_worse=True)
    ind.append(Indicator("WTI Crude Oil", wti_val, "USD/bbl", "Inflations-/Geopolitik-Barometer", wti_status))

    # 9) Gold – Yahoo
    gold = fetch_yf_last("GC=F") if use_yf else None
    gold_val = "error" if gold is None else r2(gold)
    gold_status = classify(gold_val, th(cfg, "gold"), higher_is_worse=True)
    ind.append(Indicator("Gold Futures (GC=F)", gold_val, "USD/oz", "Safe haven proxy", gold_status))

    return ind

# ----------------- ShockScore -----------------

def compute_shock_score(indicators: List[Indicator]) -> Tuple[float, Dict[str, float]]:
    """
    Hedge-Fonds-Gewichtung pro Indikator (Summe = 1.00).
    Status (green/yellow/orange/red/gray) -> 0..1 über status_to_score().
    Gesamt-Score = Summe( Gewicht_i * 100 * StatusScore_i ).
    parts liefert die Einzelbeiträge je Indikator (0..100, gewichtet).
    """

    # Gewichte pro Indikator (Summe = 1.00)
    weights = {
        "yield curve (10y–2y)": 0.20,
        "us high yield spread": 0.15,
        "us dollar index (dxy)": 0.10,
        "ust 10y yield": 0.10,
        "vix (s&p 500 volatility)": 0.10,
        "reverse repo ($bn)": 0.10,
        "s&p 500 structure (ma50 vs ma200)": 0.10,
        "wti crude oil": 0.08,
        "gold futures (gc=f)": 0.07,
    }

    def norm_name(n: str) -> str:
        return n.strip().lower()

    total = 0.0
    parts: Dict[str, float] = {}

    for i in indicators:
        n = norm_name(i.name)
        # Falls sich der exakte Name mal ändert: sanfter Fallback per Teilstring
        # (nur wenn kein exakter Treffer vorhanden ist)
        w = weights.get(n)
        if w is None:
            if "yield curve" in n and "10y" in n:
                w = weights["yield curve (10y–2y)"]
            elif "high yield" in n:
                w = weights["us high yield spread"]
            elif "dollar index" in n or "dxy" in n:
                w = weights["us dollar index (dxy)"]
            elif "ust 10y" in n or ("10y" in n and "yield" in n):
                w = weights["ust 10y yield"]
            elif "vix" in n:
                w = weights["vix (s&p 500 volatility)"]
            elif "reverse repo" in n:
                w = weights["reverse repo ($bn)"]
            elif "structure" in n or ("ma50" in n and "ma200" in n) or "s&p 500" in n:
                w = weights["s&p 500 structure (ma50 vs ma200)"]
            elif "wti" in n or "crude" in n or "oil" in n:
                w = weights["wti crude oil"]
            elif "gold" in n:
                w = weights["gold futures (gc=f)"]
            else:
                w = 0.0  # unbekannt -> kein Beitrag

        s01 = status_to_score(i.status)  # 0..1
        contrib = 100.0 * w * s01
        parts[i.name] = r2(contrib)
        total += contrib

    return r2(total), parts

# ----------------- Main -----------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--use-fred", action="store_true", help="FRED aktivieren")
    ap.add_argument("--use-yf", action="store_true", help="Yahoo Finance aktivieren")
    ap.add_argument("--out", type=str, default="out", help="Output-Ordner")
    args = ap.parse_args()

    ensure_dir(args.out)

    # (Optional) Hier könnte ein YAML-Config geladen werden — wir nutzen Defaults:
    cfg: Dict[str, Any] = DEFAULT_CFG

    indicators = build_indicators(args.use_fred, args.use_yf, cfg)
    total_score, parts = compute_shock_score(indicators)

    now = datetime.now(ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%d %H:%M %Z")

    # JSON
    report = {
        "as_of": now,
        "total_score": total_score,
        "score_parts": parts,
        "indicators": [
            {
                **asdict(i),
                "display_value": fmt2(i.value, f" {i.unit}" if i.unit else ""),
            }
            for i in indicators
        ],
    }

    json_path = os.path.join(args.out, "shock_dashboard.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Markdown
    md_lines: List[str] = []
    md_lines.append(f"# Shock Dashboard — {now}")
    md_lines.append(f"**Total Shock Score:** {fmt2(total_score)}/100\n")
    md_lines.append("## Indicators")
    for i in indicators:
        md_lines.append(
            f"- {status_emoji(i.status)} **{i.name}**: {fmt2(i.value)} {i.unit} — {i.comment}"
        )
    md_lines.append("\n## Score by Bucket")
    for k, v in parts.items():
        md_lines.append(f"- **{k}**: {fmt2(v)}")

    md_path = os.path.join(args.out, "shock_dashboard.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print("Saved:")
    print(" ", json_path)
    print(" ", md_path)

if __name__ == "__main__":
    main()