#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PIEN'S MACRO SHOCK DASHBOARD (Python)
-------------------------------------
Fetches macro indicators, computes a "Shock Score", and writes a daily report.
- Designed to be robust: uses online sources if possible; falls back to local values if not.
- Configure thresholds/weights in config.yaml.
- Run:  python shock_dashboard.py --out out/ --use-fred --use-yf
Author: ChatGPT (for Pien)
"""

import os
import sys
import argparse
import json
import yaml
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime
from zoneinfo import ZoneInfo

try:
    import requests
except Exception:
    requests = None

try:
    import yfinance as yf
except Exception:
    yf = None

def pct(x):
    try:
        return f"{float(x):.2f}%"
    except Exception:
        return str(x)

def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def read_local_fallback(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def fetch_fred_series(series_id: str, api_key: Optional[str]=None) -> Optional[float]:
    if requests is None:
        return None
    key = api_key or os.environ.get("FRED_API_KEY", "")
    try:
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": series_id,
            "api_key": key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 1
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        obs = data.get("observations", [])
        if not obs: return None
        val = obs[0].get("value", None)
        if val in (".", "", None): return None
        return float(val)
    except Exception:
        return None

def fetch_yfinance_last(symbol: str) -> Optional[float]:
    if yf is None:
        return None
    try:
        t = yf.Ticker(symbol)
        data = t.history(period="5d", interval="1d")
        if data is None or data.empty: return None
        return float(data["Close"].iloc[-1])
    except Exception:
        return None

def fetch_yfinance_ma(symbol: str, window: int) -> Optional[float]:
    if yf is None:
        return None
    try:
        t = yf.Ticker(symbol)
        data = t.history(period="1y", interval="1d")
        if data is None or data.empty: return None
        ma = data["Close"].rolling(window=window).mean().iloc[-1]
        return float(ma)
    except Exception:
        return None

from dataclasses import dataclass

@dataclass
class Indicator:
    name: str
    value: Optional[float]
    unit: str
    comment: str
    status: str  # "green", "yellow", "orange", "red"

def classify(value: Optional[float], rules: Dict[str, Any], default_status="yellow") -> str:
    if value is None:
        return default_status
    try:
        if "red_gt" in rules and value > rules["red_gt"]: return "red"
        if "red_lt" in rules and value < rules["red_lt"]: return "red"
        if "orange_gt" in rules and value > rules["orange_gt"]: return "orange"
        if "orange_lt" in rules and value < rules["orange_lt"]: return "orange"
        if "yellow_gt" in rules and value > rules["yellow_gt"]: return "yellow"
        if "yellow_lt" in rules and value < rules["yellow_lt"]: return "yellow"
        return "green"
    except Exception:
        return default_status

def build_indicators(cfg: Dict[str, Any], use_fred: bool, use_yf: bool, fallback_vals: Dict[str, Any]) -> List[Indicator]:
    ind = []

    # 1) Yield Curve (10Y - 2Y)
    yc_val = None
    if use_fred:
        dgs10 = fetch_fred_series("DGS10", api_key=os.environ.get("FRED_API_KEY"))
        dgs2 = fetch_fred_series("DGS2", api_key=os.environ.get("FRED_API_KEY"))
        if dgs10 is not None and dgs2 is not None:
            yc_val = dgs10 - dgs2
    if yc_val is None:
        yc_val = fallback_vals.get("yield_curve_spread", 0.5)
    yc_status = classify(yc_val, cfg["thresholds"]["yield_curve"])
    ind.append(Indicator("Yield Curve (10Y-2Y)", yc_val, "%", "Positive = normal, negative = inversion", yc_status))

    # 2) DXY
    dxy_val = None
    if use_yf:
        dxy_val = fetch_yfinance_last("DX-Y.NYB") or fetch_yfinance_last("DXY")
    if dxy_val is None:
        dxy_val = fallback_vals.get("dxy", 108.0)
    dxy_status = classify(dxy_val, cfg["thresholds"]["dxy"])
    ind.append(Indicator("US Dollar Index (DXY)", dxy_val, "", "Starker USD belastet Risikoassets", dxy_status))

    # 3) UST 10Y
    ust10 = None
    if use_fred:
        ust10 = fetch_fred_series("DGS10", api_key=os.environ.get("FRED_API_KEY"))
    if ust10 is None:
        ust10 = fallback_vals.get("ust10", 5.0)
    ust10_status = classify(ust10, cfg["thresholds"]["ust10"])
    ind.append(Indicator("UST 10Y Yield", ust10, "%", "Hohe Renditen drücken Bewertungen", ust10_status))

    # 4) UST 30Y
    ust30 = None
    if use_fred:
        ust30 = fetch_fred_series("DGS30", api_key=os.environ.get("FRED_API_KEY"))
    if ust30 is None:
        ust30 = fallback_vals.get("ust30", 5.1)
    ust30_status = classify(ust30, cfg["thresholds"]["ust30"])
    ind.append(Indicator("UST 30Y Yield", ust30, "%", "Langfristvertrauen / Duration-Risiko", ust30_status))

    # 5) VIX
    vix_val = None
    if use_yf:
        vix_val = fetch_yfinance_last("^VIX")
    if vix_val is None:
        vix_val = fallback_vals.get("vix", 28.0)
    vix_status = classify(vix_val, cfg["thresholds"]["vix"])
    ind.append(Indicator("VIX (S&P 500 Volatility)", vix_val, "", "Angstbarometer", vix_status))

    # 6) HY Spreads
    hy_spread = None
    if use_fred:
        hy_spread = fetch_fred_series("BAMLH0A0HYM2", api_key=os.environ.get("FRED_API_KEY"))
    if hy_spread is None:
        hy_spread = fallback_vals.get("hy_spread", 4.8)
    hy_status = classify(hy_spread, cfg["thresholds"]["hy_spread"])
    ind.append(Indicator("US High Yield Spread", hy_spread, "%", "Kreditstress", hy_status))

    # 7) Reverse Repo proxy
    rrp = None
    if use_fred:
        rrp = fetch_fred_series("RRPONTSYD", api_key=os.environ.get("FRED_API_KEY"))
    if rrp is None:
        rrp = fallback_vals.get("reverse_repo", 400.0)
    rrp_status = classify(rrp, cfg["thresholds"]["reverse_repo"])
    ind.append(Indicator("Reverse Repo ($bn)", rrp, "bn", "Liquiditätsparkplatz; starker Rückgang = Abzug", rrp_status))

    # 8) S&P 500 MA structure
    ma50 = None; ma200 = None
    if use_yf:
        ma50 = fetch_yfinance_ma("^GSPC", 50)
        ma200 = fetch_yfinance_ma("^GSPC", 200)
    if ma50 is None or ma200 is None:
        ma50 = fallback_vals.get("spx_ma50", 5200.0)
        ma200 = fallback_vals.get("spx_ma200", 5000.0)
    diff = float(ma50 - ma200)
    spx_status = classify(diff, cfg["thresholds"]["spx_ma_cross"])
    ind.append(Indicator("S&P 500 Structure (MA50 vs MA200)", diff, "pts", "Death Cross < 0", spx_status))

    # 9) Oil (WTI)
    wti = None
    if use_yf:
        wti = fetch_yfinance_last("CL=F")
    if wti is None:
        wti = fallback_vals.get("wti", 94.0)
    wti_status = classify(wti, cfg["thresholds"]["wti"])
    ind.append(Indicator("WTI Crude Oil", wti, "USD/bbl", "Inflations-/Geopolitik-Barometer", wti_status))

    # 10) Gold & Silver
    gold = None; silver = None
    if use_yf:
        gold = fetch_yfinance_last("GC=F")
        silver = fetch_yfinance_last("SI=F")
    if gold is None: gold = fallback_vals.get("gold", 2560.0)
    if silver is None: silver = fallback_vals.get("silver", 28.0)
    gold_status = classify(gold, cfg["thresholds"]["gold"])
    silver_status = classify(silver, cfg["thresholds"]["silver"])
    ind.append(Indicator("Gold Futures (GC=F)", gold, "USD/oz", "Safe haven proxy", gold_status))
    ind.append(Indicator("Silver Futures (SI=F)", silver, "USD/oz", "Industrial+safe haven", silver_status))

    return ind

def compute_shock_score(indicators, cfg):
    weights = cfg["weights"]
    buckets = {
        "Yield Curve (10Y-2Y)": "bonds",
        "UST 10Y Yield": "bonds",
        "UST 30Y Yield": "bonds",
        "US Dollar Index (DXY)": "fx",
        "VIX (S&P 500 Volatility)": "vol",
        "US High Yield Spread": "credit",
        "Reverse Repo ($bn)": "liquidity",
        "S&P 500 Structure (MA50 vs MA200)": "equity",
        "WTI Crude Oil": "commod",
        "Gold Futures (GC=F)": "alts",
        "Silver Futures (SI=F)": "alts",
    }
    bucket_vals = {k: [] for k in weights.keys()}
    for i in indicators:
        b = buckets.get(i.name)
        if b in bucket_vals:
            # map status to score 0-1
            s = {"green":0.0, "yellow":0.5, "orange":0.75, "red":1.0}.get(i.status, 0.5)
            bucket_vals[b].append(s)
    parts = {}
    total = 0.0
    for b, arr in bucket_vals.items():
        if not arr: 
            continue
        avg = sum(arr)/len(arr)
        part = avg * weights[b]
        parts[b] = part
        total += part
    total_score = round(total * 100, 2)
    return total_score, parts

def status_emoji(status: str) -> str:
    return {"green":"🟢", "yellow":"🟡", "orange":"🟠", "red":"🔴"}.get(status, "🟡")

def main():
    import pandas as pd
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--fallback", default="fallback_values.yaml")
    ap.add_argument("--out", default="out")
    ap.add_argument("--use-fred", action="store_true")
    ap.add_argument("--use-yf", action="store_true")
    args = ap.parse_args()

    ensure_dir(args.out)
    cfg = load_yaml(args.config)
    fallback_vals = read_local_fallback(args.fallback)

    indicators = build_indicators(cfg, args.use_fred, args.use_yf, fallback_vals)
    total_score, parts = compute_shock_score(indicators, cfg)

    now = datetime.now(ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%d %H:%M %Z")
    report = {
        "as_of": now,
        "total_score": total_score,
        "score_parts": parts,
        "indicators": [asdict(i) for i in indicators],
    }

    json_path = os.path.join(args.out, "shock_dashboard.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    rows = []
    for i in indicators:
        rows.append({
            "as_of": now,
            "indicator": i.name,
            "value": i.value,
            "unit": i.unit,
            "status": i.status,
            "comment": i.comment
        })
    df = pd.DataFrame(rows)
    csv_path = os.path.join(args.out, "shock_dashboard.csv")
    df.to_csv(csv_path, index=False)

    md_lines = []
    md_lines.append(f"# Shock Dashboard — {now}")
    md_lines.append(f"**Total Shock Score:** {total_score}/100\n")
    md_lines.append("## Indicators")
    for i in indicators:
        md_lines.append(f"- {status_emoji(i.status)} **{i.name}**: {i.value} {i.unit} — {i.comment}")
    md_lines.append("\n## Score by Bucket")
    for k, v in parts.items():
        md_lines.append(f"- **{k}**: {round(v*100,2)}")
    md = "\n".join(md_lines)
    md_path = os.path.join(args.out, "shock_dashboard.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Saved:\n- {json_path}\n- {csv_path}\n- {md_path}")

if __name__ == "__main__":
    main()
