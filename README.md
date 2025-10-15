# PIEN'S MACRO SHOCK DASHBOARD — Python

Dieses Set liefert dir ein **Frühwarn-Dashboard** für Makro-Schocks.
# 📊 Shock Dashboard — ReadMe

Das **Shock Dashboard** misst täglich den Stress- und Risiko-Zustand der globalen Finanzmärkte.  
Es kombiniert 10+ Makro-Indikatoren zu einem Gesamtscore zwischen **0 und 100 Punkten**:
## 🧠 TEIL 1 — Erklärungen der einzelnen Indikatoren

### **1️⃣ Yield Curve (10Y–2Y)**
Misst den Unterschied zwischen 10-jährigen und 2-jährigen US-Staatsanleihen.  
Normalerweise ist die 10-jährige Rendite höher als die 2-jährige, da langfristige Anlagen riskanter sind.  
Wenn die Kurve **invertiert** (also 2Y > 10Y), deutet das auf eine bevorstehende Rezession hin.  
➡️ **Signalisiert Vertrauen oder Misstrauen in die langfristige Wirtschaftsentwicklung.**

---

### **2️⃣ US Dollar Index (DXY)**
Vergleicht die Stärke des US-Dollars gegenüber den wichtigsten Weltwährungen (EUR, JPY, GBP usw.).  
Ein **starker Dollar** zieht Kapital in die USA und belastet Rohstoffe & Emerging Markets.  
Ein **schwächerer Dollar** signalisiert Risikofreude und unterstützt weltweite Kapitalflüsse.  
➡️ **Zeigt globale Risiko- und Liquiditätstrends.**

---

### **3️⃣ UST 10Y Yield**
Die Rendite 10-jähriger US-Staatsanleihen ist die wichtigste globale Benchmark für Finanzierungskosten.  
Steigende Zinsen erhöhen die Kreditkosten und senken die Bewertungen von Aktien und Immobilien.  
➡️ **Spiegelt das allgemeine Zins- und Bewertungsniveau wider.**

---

### **4️⃣ UST 30Y Yield**
Die 30-jährige Rendite zeigt das langfristige Vertrauen der Märkte in Preisstabilität und Wirtschaftswachstum.  
Wenn sie stark steigt, erwarten Investoren höhere Inflation oder geringeres Vertrauen in die Fed.  
➡️ **Langfristiges Vertrauens- und Inflationsbarometer.**

---

### **5️⃣ VIX (Volatility Index)**
Der VIX misst die erwartete Schwankungsbreite des S&P 500 – also die „Marktangst“.  
Hohe Werte deuten auf Unsicherheit und Verkaufsdruck hin, niedrige auf Stabilität.  
➡️ **Direktes Barometer für Angst oder Gelassenheit an den Aktienmärkten.**

---

### **6️⃣ US High Yield Spread**
Zeigt den Risikoaufschlag zwischen Unternehmensanleihen (Junk Bonds) und sicheren US-Staatsanleihen.  
Wenn der Spread steigt, meiden Investoren riskante Schuldner → Liquidität zieht sich zurück.  
➡️ **Misst Kreditstress und Finanzierungsbedingungen.**

---

### **7️⃣ Reverse Repo ($ bn)**
Gibt an, wie viel Geld Banken täglich bei der Fed parken.  
Sinkt dieser Wert stark, ziehen Banken Geld aus dem Markt → weniger Liquidität.  
➡️ **Indikator für System-Liquidität und Vertrauen in Geldmärkte.**

---

### **8️⃣ S&P 500 Structure (MA50–MA200)**
Technischer Trendindikator: misst den Abstand zwischen dem 50-Tage- und dem 200-Tage-Durchschnitt.  
Wenn MA50 < MA200, spricht man von einem „Death Cross“ (Abwärtstrend).  
➡️ **Zeigt, ob der Aktienmarkt strukturell bullisch oder bärisch ist.**

---

### **9️⃣ WTI Crude Oil**
Der Ölpreis beeinflusst fast alle Preise weltweit.  
Zu niedrige Preise deuten auf schwache Nachfrage → Rezession.  
Zu hohe Preise führen zu Inflation → Wachstumsbremse.  
➡️ **Inflations- und Energiebarometer der Weltwirtschaft.**

---

### **🔟 Gold Futures**
Gold gilt als „sicherer Hafen“.  
Steigende Preise zeigen Risikoaversion und Misstrauen gegenüber Finanzsystemen.  
➡️ **Misst die Flucht in Sicherheit und das Vertrauen in Währungen.**

---

### **1️⃣1️⃣ Silver Futures**
Silber ist teils Industriemetall (Wachstum), teils Edelmetall (Sicherheit).  
Reagiert daher auf **Wirtschaftsdaten UND Krisenstimmung**.  
➡️ **Hybrid-Indikator zwischen Risiko- und Sicherheitsverhalten.**

---

## ⚙️ TEIL 2 — Schwellenwerte & Farbbereiche

| Nr. | Indikator | 🟢 Günstig / Normal | 🟡 Neutral / Übergang | 🔴 Risiko / Stress | Bedeutung |
|:--:|------------|--------------------|----------------------|-------------------|------------|
| **1** | Yield Curve (10Y–2Y) | > 0.3 % | 0 – 0.3 % | < 0 % | Inversion = Rezessionssignal |
| **2** | US Dollar Index (DXY) | < 102 | 102 – 106 | > 106 | Starker USD belastet Risikoassets |
| **3** | UST 10Y Yield | < 3.5 % | 3.5 – 4.5 % | > 4.5 % | Hohe Renditen = Bewertungsdruck |
| **4** | UST 30Y Yield | < 4.0 % | 4.0 – 5.0 % | > 5.0 % | Langfristige Inflationserwartung |
| **5** | VIX | < 20 | 20 – 25 | > 25 | Angstbarometer – >25 = Panik |
| **6** | High Yield Spread | < 4 % | 4 – 6 % | > 6 % | Kreditstress in Risikoanleihen |
| **7** | Reverse Repo | stabil / steigend | leicht fallend | stark fallend | Liquiditätsabzug |
| **8** | S&P 500 (MA50–MA200) | > 0 | – | < 0 | Trend: Bullish vs Death Cross |
| **9** | WTI Oil | 60 – 100 $ | – | < 50 $ / > 120 $ | Nachfrage vs Inflationsdruck |
| **10** | Gold | < 2200 $ | 2200 – 2800 $ | > 2800 $ | Flucht in Sicherheit |
| **11** | Silber | < 30 $ | 30 – 40 $ | > 40 $ | Überhitzte Spekulation / Defensivphase |

---

| Bereich | Bedeutung |
|----------|------------|
| **0 – 40 🟢** | Stabile Marktphase, Risikoappetit vorhanden |
| **40 – 60 🟡** | Erhöhte Wachsamkeit, erste Anzeichen von Stress |
| **60 – 80 🟠** | Risikoaversion nimmt zu, Cash bevorzugen |
| **80 – 100 🔴** | Systemischer Stress / Schockgefahr |

---

## ⚙️ Funktionsweise
Das Script sammelt Live-Daten (FRED + Yahoo Finance), berechnet aus Schwellenwerten eine Teilnote pro Indikator und fasst diese zu einem „Shock-Score“ zusammen.  
Fehlen Live-Daten, nutzt es die Fallback-Datei `fallback_values.yaml`.

---

## 📈 Indikatoren-Übersicht

## 📊 Indikatoren – Erklärung und Schwellenwerte

Jeder Indikator misst einen anderen Aspekt des globalen Finanzsystems.  
Die Farben 🟢🟡🔴 zeigen an, ob der aktuelle Wert **positiv, neutral oder riskant** für die Märkte ist.

| Nr. | Indikator | Beschreibung | Farbbereiche / Schwellen | Interpretation |
|:--:|------------|---------------|---------------------------|----------------|
| **1** | **Yield Curve (10Y–2Y)** | Misst den Unterschied zwischen 10-jährigen und 2-jährigen  	US-Staatsanleihen. Eine „inverse Zinskurve“ (kurzfristige Zinsen > langfristige) gilt 		als klassisches Rezessionssignal. 						     	| 🔴 **< 0 %** → Inversion<br>									  🟡 **0 – 0.3 %** → flach<br>									  🟢 **> 0.3 %** → normal 							| Negativer Wert signalisiert Rezessionsgefahr,positiver Wert steht für gesunde Wachstums­erwartungen. |
| **2** | **US Dollar Index (DXY)** | Zeigt die Stärke des US-Dollars gegenüber einem Korb 		 wichtiger Währungen (EUR, JPY, GBP …). 						                  	| 🟢 **< 102** → schwacher USD = Risikofreude<br>						🟡 **102 – 106** → neutral<br>									🔴 **> 106** → starker USD = Risk-Off 						     | Ein starker Dollar entzieht global Liquidität (belastet Rohstoffe & Emerging Markets). Ein schwächerer Dollar fördert Risikoappetit. |
| **3** | **UST 10Y Yield** | Rendite 10-jähriger US-Staatsanleihen – der wichtigste globale Referenzzins. | 🟢 **< 3.5 %** → günstig<br>🟡 **3.5 – 4.5 %** → neutral<br>🔴 **> 4.5 %** → hoch | Hohe Renditen bedeuten teureres Kapital und Bewertungsdruck für Aktien, Immobilien und Risikoassets. |
| **4** | **UST 30Y Yield** | Langfristzins – spiegelt Inflationserwartung und Vertrauen in die Wirtschaft auf 30 Jahre. | 🟢 **< 4.0 %** → stabile Inflationserwartung<br>🟡 **4.0 – 5.0 %** → neutral<br>🔴 **> 5.0 %** → Inflationssorgen | Steigende Langfristzinsen signalisieren weniger Vertrauen in langfristige Preisstabilität. |
| **5** | **VIX (S&P 500 Volatility)** | Zeigt, wie stark der US-Aktienmarkt kurzfristig schwankt – das „Angstbarometer“ der Börse. | 🟢 **< 20** → ruhig<br>🟡 **20 – 25** → zunehmende Unsicherheit<br>🔴 **> 25** → Panik | Je höher der VIX, desto größer die erwarteten Marktbewegungen. Über 25 = Stress. |
| **6** | **US High Yield Spread** | Aufschlag von „Junk Bonds“ (hohes Risiko) gegenüber sicheren US-Staatsanleihen. | 🟢 **< 4 %** → stabil<br>🟡 **4 – 6 %** → mittlerer Stress<br>🔴 **> 6 %** → Kreditkrise droht | Ein steigender Spread zeigt, dass Investoren Risikoanleihen meiden → Kreditverknappung. |
| **7** | **Reverse Repo ($ bn)** | Geldmenge, die Banken täglich bei der FED parken. Zeigt, wie viel überschüssige Liquidität im System steckt. | 🟢 **stabil / steigend** → Liquidität reichlich<br>🔴 **schnell fallend** → Abzug | Wenn der Wert stark fällt, ziehen Banken Geld aus dem Markt → weniger Liquidität, höheres Risiko. |
| **8** | **S&P 500 Structure (MA50 – MA200)** | Technischer Indikator: Abstand zwischen 50-Tage- und 200-Tage-Durchschnitt. | 🔴 **< 0 pts** → „Death Cross“ (Abwärtstrend)<br>🟢 **> 0 pts** → „Golden Cross“ (Aufwärtstrend) | Zeigt, ob der Aktienmarkt strukturell bullisch oder bärisch ausgerichtet ist. |
| **9** | **WTI Crude Oil ($/bbl)** | Preis für US-Rohöl – Indikator für Energie-, Nachfrage- und Inflationsdruck. | 🟢 **60 – 100 $** → normal<br>🔴 **< 50 $ oder > 120 $** → Stress | Sehr niedrige Preise = Nachfrageschwäche / Rezession; sehr hohe = Inflationsdruck & Angebotskrisen. |
| **10** | **Gold Futures ($/oz)** | Sicherer Hafen („Safe Haven“) – steigt bei Misstrauen in Finanzsysteme. | 🟢 **< 2200 $** → ruhig<br>🟡 **2200 – 2800 $** → moderat defensiv<br>🔴 **> 2800 $** → Krisenmodus | Hohe Goldpreise zeigen Kapitalflucht in Sicherheit → Vertrauensverlust im Finanzsystem. |
| **11** | **Silver Futures ($/oz)** | Silber ist teils Industriemetall, teils Wertspeicher – reagiert auf Risiko UND Wirtschaftsdaten. | 🟢 **< 30 $** → normal<br>🟡 **30 – 40 $** → wachsam<br>🔴 **> 40 $** → überhitzt | Hohe Preise deuten auf Spekulation oder Flucht in Sachwerte hin. |

---

## 🧭 Kurz gesagt
| Kategorie | Bedeutung |
|------------|------------|
| **🟢 Grün** | Gesund / Entspannt – Märkte funktionieren normal |
| **🟡 Gelb** | Frühwarnzone – Risiko nimmt leicht zu |
| **🔴 Rot** | Gefahr – Marktstress oder Schockindikator |

---

## 🧭 Interne Gruppierung („Buckets“)
| Bucket | Inhalt | Zweck |
|---------|---------|-------|
| **bonds** | Renditen & Zinskurve | Zinsstress |
| **fx** | US-Dollar | Währungsdruck |
| **vol** | VIX | Marktangst |
| **credit** | High-Yield-Spreads | Kreditmärkte |
| **liquidity** | Reverse Repo | System-Liquidität |
| **equity** | S&P 500 Structure | Aktientechnik |
| **commod** | Öl | Rohstoffmärkte |
| **alts** | Gold & Silber | Flucht-Assets |

---

## 🟢🟡🟠🔴 Farblogik
| Farbe | Punkte-Range | Bedeutung |
|--------|---------------|------------|
| 🟢 Green | 0 – 40 | Normal / stabil |
| 🟡 Yellow | 40 – 60 | Vorsicht, Übergang |
| 🟠 Orange | 60 – 80 | Risiko steigt |
| 🔴 Red | 80 – 100 | Hoher Stress / Schockphase |

---

## 🧠 Nutzung
1. **Start**: per `Start_Shock_Dashboard.command` oder `python shock_dashboard.py --use-fred --use-yf --out out/`  
2. **Ergebnis**:  
   - Kurzfassung im Terminal  
   - Langfassung als `out/shock_dashboard.md`  
   - Historie im `out/`-Archiv  
3. **Interpretation**:  
   - Score < 40 → Markt ruhig  
   - 40 – 60 → Wachsam bleiben  
   - > 60 → Cash, Absicherung oder Defensivsektor  
4. **Cron-Jobs** aktualisieren automatisch morgens + abends.

---

## 🧩 Hinweise
- Warnungen zu „OpenSSL/urllib3“ sind **harmlos**.  
- Bei Internet-Ausfall werden Fallback-Werte aus `fallback_values.yaml` genutzt.  
- Zeitzone: **Europe/Berlin**, lokale Zeit.

---

## 🔒 Beispiel-Ausgabe
## Dateien
- `shock_dashboard.py` — Hauptskript
- `config.yaml` — Schwellwerte & Gewichte
- `fallback_values.yaml` — Offline/Backup-Werte
- `out/` — Output-Ordner

## Installation
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install yfinance requests pandas pyyaml
```

Optional: FRED-API-Key setzen:7e5defb1c15ea4f7df0aeac4d6c1ff2e
```bash
export FRED_API_KEY=DEIN_KEY   # Windows: set FRED_API_KEY=DEIN_KEY
```

## Nutzung
**Offline/Fallback:**
```bash
python shock_dashboard.py --out out/
```

**Online (FRED + yfinance):**
```bash
python shock_dashboard.py --use-fred --use-yf --out out/
```

## Automatisierung (täglich 07:30)
macOS/Linux (cron):
```bash
crontab -e
30 7 * * * /usr/bin/env bash -lc 'cd /PATH/zu/shock_dashboard && .venv/bin/python shock_dashboard.py --use-fred --use-yf --out out/ >> cron.log 2>&1'
```

## Interpretation
- 0–40: Stabil
- 40–60: Erhöhte Spannung
- 60–80: Akute Risiko-Phase
- >80: Systemschock

Viel Erfolg ✊
