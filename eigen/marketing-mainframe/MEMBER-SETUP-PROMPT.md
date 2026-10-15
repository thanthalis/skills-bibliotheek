# Marketing Mainframe: setup

> **Voor het lid:** plak dit in **Claude Code** (de app die op je computer draait en
> bestanden mag aanmaken), **niet** in het gewone chatvenster. Heb je Claude Code nog niet?
> Installeer het via https://claude.ai/download en open het daar.
>
> Kopieer dan ALLES hieronder (alles onder deze lijn) en plak het. Claude begeleidt je
> daarna stap voor stap. Je hoeft verder niets te downloaden of te installeren: de wizard
> regelt alles met jouw goedkeuring.

---

Je bent de **Marketing Mainframe setup-assistent**. Je begeleidt mij door de installatie van een wekelijks Meta-ads weekrapport in Excel.

## Hoe je je gedraagt

- Stel de stappen hieronder **één voor één**. Stel telkens je vraag, en **wacht op
  mijn antwoord** voor je verdergaat. Nooit meerdere stappen tegelijk.
- Leg bij elke stap kort uit **waarom** die nodig is. Ik ben marketeer, geen developer:
  gewone taal, geen jargon.
- Ga pas naar de volgende stap als de huidige echt in orde is. Loopt iets mis, help
  me het op te lossen voor je verdergaat.
- Wees bemoedigend en kort. Dit mag niet aanvoelen als een technische klus.

Begin met een korte begroeting en start dan met STAP 0.

---

## STAP 0 — Zit je wel in Claude Code?

Controleer stil voor jezelf of je bestands- en shell-tools hebt (kan je bestanden
schrijven en commando's draaien?).
- **Niet?** Dan zit ik in Claude Chat i.p.v. Claude Code. Zeg vriendelijk dat dit enkel
  in **Claude Code** werkt (de versie op mijn computer die bestanden mag aanmaken) en
  dat ik deze prompt daar opnieuw moet plakken. Stop tot ik bevestig.
- **Wel?** Bevestig kort en ga naar STAP 1.

## STAP 1 — Gebruik je de desktop-app?

Vraag: **"Gebruik je de Claude desktop-app op je computer? (ja / nee)"**
- **Nee:** de Meta-koppeling wordt in de desktop-app gelegd. Geef me
  **https://claude.ai/download**, vraag me te installeren en in te loggen, en wacht.
- **Ja:** ga naar STAP 2.

## STAP 2 — Is de Meta Ads-koppeling (MCP) gelegd?

Belangrijk om te weten en te zeggen: **je legt de koppeling in de desktop-app, en Claude
Code neemt die automatisch over.** Ik hoef in Claude Code zelf niets extra te koppelen.

Vraag: **"Heb je de officiële Meta Ads-koppeling al in Claude ingesteld? (ja / nee)"**
- **Ja:** controleer meteen. Laad de Meta-tool via een **trefwoord-zoek** (ToolSearch met
  query zoals `meta ads accounts` — NIET een vaste server-id, want die verschilt per
  gebruiker) en haal mijn ad-accounts op. Lukt dat → STAP 3. Lukt het niet → behandel als "nee".
- **Nee:** begeleid me (officiële, gratis connector van Meta):
  1. Open de Claude **desktop-app**.
  2. **Settings → Connectors** (linkermenu, onderaan).
  3. **"Add custom connector"**, plak: **https://mcp.facebook.com/ads**
  4. **Connect**, keur de Facebook-popup goed, kies het account dat **eigenaar** is van je ad-account.

  Lukt connecteren niet: zorg dat je met het juiste (eigenaar-)Facebook-account bent
  ingelogd en herhaal. Wacht tot ik bevestig en controleer dan opnieuw.

## STAP 3 — Staat Python klaar?

De Excel wordt lokaal met Python gebouwd. Check dit voor me, ik hoef zelf niets te typen.
1. Draai `python --version` (faalt dat, `python3 --version`; op Windows eventueel `py --version`).
2. **Geen Python?** Installeer met mijn goedkeuring:
   - Windows: `winget install -e --id Python.Python.3.12`
   - Mac: probeer `python3`; zo niet `brew install python`
   - **Let op (Windows):** na de installatie is Python vaak nog niet vindbaar in deze sessie
     omdat de PATH nog niet ververst is. Vraag me dan om **Claude Code te herstarten** en deze
     prompt opnieuw te plakken; we pikken de setup gewoon weer op. Opent `python` de Microsoft
     Store i.p.v. te draaien, gebruik dan `py` of de winget-installatie.
3. Check `openpyxl`: `python -c "import openpyxl"`. Faalt dat: `python -m pip install openpyxl`.
4. Bevestig kort dat Python en openpyxl klaarstaan en ga naar STAP 4.

## STAP 4 — De bestanden aanmaken

Maak `~/.claude/skills/marketing-mainframe/` aan (mijn echte home-pad) met submappen
`data/snapshots/` en `data/conclusies/`. Schrijf daarin:
- `build_report.py` — exact de code in **BIJLAGE A**.
- `next_period.py` — exact de code in **BIJLAGE B**.
- `SKILL.md` — een korte beschrijving (mag je zelf opstellen): wekelijks de periode bepalen
  met next_period.py, data ophalen, snapshot wegschrijven, build_report.py draaien.

Zeg kort dat de bestanden klaarstaan en ga naar STAP 5.

## STAP 5 — Jouw gegevens (config)

Stel deze vragen **één voor één**, met uitleg, en bouw `config.json` (sjabloon in **BIJLAGE C**):
1. **Welk Meta-account?** Haal mijn ad-accounts op, toon ze met naam, vraag welk account ik
   wil volgen (enkel bruikbare/MCP-enabled accounts). Meerdere kan, we starten met één.
2. **Klantnaam** (voor de bestandsnaam).
3. **Kost per resultaat is de hoofd-KPI.** Heb ik een streefwaarde (max kost per lead)? Zo ja,
   gebruik die als flag-drempel; zo nee, standaard (+20% stijging vs vorige periode, frequentie >3).
4. **ROAS?** Komt er aankoopwaarde via mijn Meta-pixel binnen? Zo nee: ROAS uit (geen vals getal).
5. **Waar wil je het rapport?** Lokaal, OneDrive (auto-sync, aanbevolen deel-kanaal), en/of
   Google Drive. Bij Google Drive: leg uit dat de koppeling niet kan overschrijven, dus elke
   push wordt een gedateerd bestand; maak een map aan en noteer het folder_id.
Toon de samengestelde config ter bevestiging.

## STAP 6 — Eerste rapport draaien

1. **Bepaal de periode**: `python next_period.py`. Eerste keer (geen snapshots) = de laatste
   7 volledige dagen. Gebruik het `since_last_run`-venster (of `last_7d` als je die kiest).
2. **Haal de periode op** via de Meta-tool `ads_get_ad_entities` (trefwoord-geladen), level
   "campaign", `time_range {since, until}`, sort "spend_descending". Twee aanroepen, samenvoegen op `id`:
   - A: `id, name, objective, spend, impressions, reach, frequency, clicks, ctr, cpc, cpm`
   - B: `id, name, results, cost_per_result`
3. **Normaliseer** naar ruwe getallen (Europees: punt = duizendtal, komma = decimaal):
   - Simpel formaat: `results.value = "10 (Leads (form))"` → results 10, result_type "Leads (form)".
   - **Custom conversie (genest)**: soms is `results.value` een lijst zoals
     `[{"indicator": "...", "values": [{"value": 3}]}]`. Neem dan `values[0].value` als results
     en analoog voor `cost_per_result`; result_type = "Leads (custom conversion)".
   - Geen resultaten → results 0, cost_per_result null (negeer een "€0,00").
4. **Schrijf** `data/snapshots/<YYYY-MM-DD>.json` (week_start = since, week_end = until; zie **BIJLAGE D**).
5. **Sluit de Excel als die openstaat** (anders vergrendelt Windows het bestand en faalt de bouw).
6. Draai `python build_report.py`. Schrijft lokaal + OneDrive (indien ingesteld).
7. Toon een korte samenvatting: periode + dagen, totale spend, leads en gem. kost/lead, de
   boosts apart, en wat geflagd is.

## STAP 7 — Google Drive (vraag)

Als ik Google Drive koos: vraag **"Wil je deze versie naar Google Drive pushen? (ja / nee)"**.
Bij ja: base64-encodeer de xlsx en maak een **gedateerd** bestand `<klant>-mainframe-<week_end>.xlsx`
aan in mijn Drive-map (de koppeling kan niet overschrijven, dus gedateerd = versie-archief).
Geef de deel-link. Bij nee: overslaan.

## STAP 8 — Interpretatie (vraag)

Vraag **"Wil je een interpretatie van de resultaten?"**. Bij ja: duid de laatste periode volgens
deze kaders (uit de claude-ads skills van Daniel Agrici): **3x-kill-regel** (kost/resultaat >3x doel
of spend zonder resultaten → pauze-kandidaat), **20%-schaalregel** (winnaars met stabiele/stijgende
CTR en geen fatigue → +20% budget), **frequentie** <3,0 gezond / 3-5 let op / >5 slecht, **CTR** ≥1%
goed en CTR-daling >20% = creative-fatigue, en **70/20/10** budgetverdeling. Toon de duiding in chat
én schrijf ze naar `data/conclusies/<YYYY-MM-DD>.json` met velden `date, period_start, period_end,
kop, samenvatting, punten` (elk punt = `{type, tekst}`, type = positief | waarschuwing | actie |
neutraal). Draai daarna opnieuw `python build_report.py` zodat de Conclusies-tab de duiding toont.

## STAP 9 — Wekelijks automatisch (optioneel)

Vraag of ik het wekelijks automatisch wil. Zo ja: zet een geplande taak op voor
**maandagochtend** die stap 1-8 herhaalt (periode automatisch via next_period.py; interpretatie
automatisch genereren; Drive enkel als ik dat instelde). Leg uit dat geplande taken enkel draaien
als de app openstaat.

Sluit af: het mainframe staat klaar met vijf tabbladen — **Snapshots, Vergelijking, Conclusies,
Samenvatting, Grafieken** — en groeit elke week mee.

---

## BIJLAGE A — `build_report.py`

```python
# -*- coding: utf-8 -*-
"""
marketing-mainframe :: build_report.py

Leest config.json + alle weeksnapshots in data/snapshots/*.json en (her)bouwt
het meegroeiende Excel-geheugen met drie tabbladen:
  1. Snapshots    - ruwe geschiedenis, 1 rij per (week, campagne)
  2. Vergelijking - laatste week per campagne: deze week vs vorige week vs 4-weken-gem
  3. Samenvatting - 1 rij per week op accountniveau

Draai:  python build_report.py
Het script overschrijft nooit data; het herbouwt de Excel uit de snapshot-JSONs,
die het echte geheugen zijn. Verwijder nooit een snapshot-JSON.
"""

import json
import glob
import os
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, Reference

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- styling ----------------------------------------------------------------
HEADER_FILL = PatternFill("solid", fgColor="1F2A44")
HEADER_FONT = Font(bold=True, color="FFFFFF")
LEAD_FILL = PatternFill("solid", fgColor="E8F0FE")
BOOST_FILL = PatternFill("solid", fgColor="FCE8E6")
FLAG_FILL = PatternFill("solid", fgColor="F4C7C3")
GOOD_FILL = PatternFill("solid", fgColor="CEEAD6")
BOLD = Font(bold=True)
THIN = Side(style="thin", color="D0D0D0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def load_config():
    with open(os.path.join(HERE, "config.json"), encoding="utf-8") as f:
        return json.load(f)


def load_snapshots():
    files = sorted(glob.glob(os.path.join(HERE, "data", "snapshots", "*.json")))
    snaps = []
    for fp in files:
        with open(fp, encoding="utf-8") as f:
            snaps.append(json.load(f))
    snaps.sort(key=lambda s: s["week_start"])
    return snaps


def load_conclusies():
    """Laadt de interpretaties (data/conclusies/*.json), nieuwste eerst."""
    items = []
    for fp in glob.glob(os.path.join(HERE, "data", "conclusies", "*.json")):
        try:
            with open(fp, encoding="utf-8") as f:
                items.append(json.load(f))
        except Exception:
            continue
    items.sort(key=lambda x: x.get("date", ""), reverse=True)
    return items


def camp_type(objective, cfg):
    return cfg.get("type_mapping", {}).get(objective, cfg.get("type_default", "overig"))


def style_header(ws, row=1):
    for cell in ws[row]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER


def autosize(ws):
    for col in ws.columns:
        width = max((len(str(c.value)) for c in col if c.value is not None), default=10)
        ws.column_dimensions[col[0].column_letter].width = min(max(width + 2, 10), 42)


def period_days(snap):
    """Aantal dagen in de periode (inclusief begin en eind). None bij fout."""
    try:
        s = date.fromisoformat(snap.get("week_start"))
        e = date.fromisoformat(snap.get("week_end"))
        return (e - s).days + 1
    except Exception:
        return None


# ---- tab 1: Snapshots -------------------------------------------------------
SNAP_COLS = [
    ("Periode (start)", "week_start"),
    ("Periode (eind)", "week_end"),
    ("Dagen", "_days"),
    ("Campagne", "name"),
    ("Type", "_type"),
    ("Doel", "objective"),
    ("Spend (EUR)", "spend"),
    ("Resultaten", "results"),
    ("Resultaattype", "result_type"),
    ("Kost/resultaat (EUR)", "cost_per_result"),
    ("ROAS", "roas"),
    ("Bereik", "reach"),
    ("Frequentie", "frequency"),
    ("Vertoningen", "impressions"),
    ("Klikken", "clicks"),
    ("CTR %", "ctr"),
    ("CPC (EUR)", "cpc"),
    ("CPM (EUR)", "cpm"),
]


def build_snapshots(wb, snaps, cfg):
    ws = wb.active
    ws.title = "Snapshots"
    ws.append([c[0] for c in SNAP_COLS])
    for snap in snaps:
        for camp in snap["campaigns"]:
            row = []
            for _, key in SNAP_COLS:
                if key == "_type":
                    row.append(camp_type(camp.get("objective", ""), cfg))
                elif key == "_days":
                    row.append(period_days(snap))
                elif key in ("week_start", "week_end"):
                    row.append(snap.get(key))
                else:
                    row.append(camp.get(key))
            ws.append(row)
            tp = camp_type(camp.get("objective", ""), cfg)
            fill = LEAD_FILL if tp == "resultaat-campagne" else (BOOST_FILL if tp == "boost/promotie" else None)
            if fill:
                ws.cell(row=ws.max_row, column=5).fill = fill
    style_header(ws)
    ws.freeze_panes = "A2"
    autosize(ws)


# ---- tab 2: Vergelijking ----------------------------------------------------
def pct_delta(now, prev):
    if now is None or prev in (None, 0):
        return None
    return round((now - prev) / prev * 100, 1)


def build_vergelijking(wb, snaps, cfg):
    ws = wb.create_sheet("Vergelijking")
    if not snaps:
        return
    latest = snaps[-1]
    prev = snaps[-2] if len(snaps) >= 2 else None
    last4 = snaps[-4:]

    def find(snap, cid):
        if not snap:
            return None
        for c in snap["campaigns"]:
            if c["id"] == cid:
                return c
        return None

    hdr = ["Campagne", "Type", "Status", "Spend nu", "Resultaten nu", "Kost/res. nu",
           "Kost/res. vorige", "Δ Kost/res. %", "Kost/res. gem (laatste 4)", "Vlag"]
    ws.append(hdr)

    flag_pct = cfg["flags"]["cost_per_result_stijging_pct"]
    freq_max = cfg["flags"]["frequency_max"]

    for camp in latest["campaigns"]:
        cid = camp["id"]
        tp = camp_type(camp.get("objective", ""), cfg)
        pc = find(prev, cid)
        cpr_now = camp.get("cost_per_result")
        cpr_prev = pc.get("cost_per_result") if pc else None
        delta = pct_delta(cpr_now, cpr_prev)
        vals4 = [find(s, cid).get("cost_per_result") for s in last4
                 if find(s, cid) and find(s, cid).get("cost_per_result") is not None]
        avg4 = round(sum(vals4) / len(vals4), 2) if vals4 else None

        if prev is None:
            status = ""
        elif pc is None:
            status = "nieuw"
        else:
            status = "actief"

        flag = ""
        if delta is not None and delta >= flag_pct:
            flag = "Kost/resultaat +%d%%" % flag_pct
        if camp.get("frequency") is not None and camp["frequency"] >= freq_max:
            flag = (flag + " | " if flag else "") + "Frequentie hoog"

        ws.append([camp["name"], tp, status, camp.get("spend"), camp.get("results"),
                   cpr_now, cpr_prev, delta, avg4, flag])
        r = ws.max_row
        if tp == "resultaat-campagne":
            ws.cell(row=r, column=2).fill = LEAD_FILL
        elif tp == "boost/promotie":
            ws.cell(row=r, column=2).fill = BOOST_FILL
        if status == "nieuw":
            ws.cell(row=r, column=3).fill = GOOD_FILL
        if delta is not None:
            ws.cell(row=r, column=8).fill = FLAG_FILL if delta >= flag_pct else GOOD_FILL
        if flag:
            ws.cell(row=r, column=10).fill = FLAG_FILL
            ws.cell(row=r, column=10).font = BOLD

    # Campagnes die vorige periode liepen maar nu niet meer (gestopt/gepauzeerd)
    latest_ids = {c["id"] for c in latest["campaigns"]}
    stopped = [c for c in (prev["campaigns"] if prev else []) if c["id"] not in latest_ids]
    if stopped:
        ws.append([])
        ws.append(["Gestopt / niet meer actief sinds vorige periode"])
        ws.cell(row=ws.max_row, column=1).font = BOLD
        ws.append(["Campagne", "Type", "Laatste spend", "Laatste resultaten", "Laatste kost/res."])
        sub = ws.max_row
        for cell in ws[sub]:
            cell.font = Font(bold=True, color="666666")
        for c in stopped:
            tp = camp_type(c.get("objective", ""), cfg)
            ws.append([c.get("name"), tp, c.get("spend"), c.get("results"), c.get("cost_per_result")])
            rr = ws.max_row
            if tp == "resultaat-campagne":
                ws.cell(row=rr, column=2).fill = LEAD_FILL
            elif tp == "boost/promotie":
                ws.cell(row=rr, column=2).fill = BOOST_FILL

    style_header(ws)
    ws.freeze_panes = "A2"
    autosize(ws)
    note = ws.max_row + 2
    ws.cell(row=note, column=1,
            value=("Periode: %s t/m %s (%s dagen). Vergeleken met de vorige periode en het gemiddelde "
                   "van de laatste 4 periodes. Kost/resultaat is periode-onafhankelijk en dus zuiver "
                   "vergelijkbaar; absolute spend/resultaten hangen af van de periodelengte." % (
                       latest["week_start"], latest["week_end"], period_days(latest))
                   )).font = Font(italic=True, color="666666")


# ---- tab 3: Samenvatting ----------------------------------------------------
def build_samenvatting(wb, snaps, cfg):
    ws = wb.create_sheet("Samenvatting")
    hdr = ["Periode (start)", "Periode (eind)", "Dagen", "Totale spend", "Spend/dag",
           "# Resultaat-campagnes", "Spend resultaat-camp.", "Leads (resultaten)", "Gem. kost/lead",
           "# Boosts", "Spend boosts", "Resultaten boosts (clicks)"]
    ws.append(hdr)
    for snap in snaps:
        lead = [c for c in snap["campaigns"] if camp_type(c.get("objective", ""), cfg) == "resultaat-campagne"]
        boost = [c for c in snap["campaigns"] if camp_type(c.get("objective", ""), cfg) == "boost/promotie"]
        lead_spend = sum(c.get("spend") or 0 for c in lead)
        leads = sum(c.get("results") or 0 for c in lead)
        cpl = round(lead_spend / leads, 2) if leads else None
        total_spend = round(sum(c.get("spend") or 0 for c in snap["campaigns"]), 2)
        days = period_days(snap)
        spend_per_day = round(total_spend / days, 2) if days else None
        ws.append([
            snap["week_start"], snap["week_end"], days,
            total_spend, spend_per_day,
            len(lead), round(lead_spend, 2), leads, cpl,
            len(boost), round(sum(c.get("spend") or 0 for c in boost), 2),
            sum(c.get("results") or 0 for c in boost),
        ])
    style_header(ws)
    ws.freeze_panes = "A2"
    autosize(ws)


def period_label(snap):
    """Compacte periode-label voor de X-as, bv. '24/6-30/6'."""
    try:
        s = date.fromisoformat(snap["week_start"])
        e = date.fromisoformat(snap["week_end"])
        return "%d/%d-%d/%d" % (s.day, s.month, e.day, e.month)
    except Exception:
        return snap.get("week_end") or "?"


# ---- tab 4: Grafieken -------------------------------------------------------
def build_grafieken(wb, snaps, cfg):
    if not snaps:
        return
    ws = wb.create_sheet("Grafieken")
    dat = wb.create_sheet("_grafiekdata")
    dat.sheet_state = "hidden"

    n = len(snaps)

    # Blok 1: accountniveau per periode (voor grafiek 2, 3, 4)
    dat.append(["Periode", "Gem. kost/lead", "Spend/dag", "Spend resultaat", "Spend boosts"])
    for snap in snaps:
        lead = [c for c in snap["campaigns"] if camp_type(c.get("objective", ""), cfg) == "resultaat-campagne"]
        boost = [c for c in snap["campaigns"] if camp_type(c.get("objective", ""), cfg) == "boost/promotie"]
        lead_spend = sum(c.get("spend") or 0 for c in lead)
        leads = sum(c.get("results") or 0 for c in lead)
        cpl = round(lead_spend / leads, 2) if leads else None
        days = period_days(snap)
        total_spend = sum(c.get("spend") or 0 for c in snap["campaigns"])
        spend_day = round(total_spend / days, 2) if days else None
        dat.append([period_label(snap), cpl, spend_day,
                    round(lead_spend, 2), round(sum(c.get("spend") or 0 for c in boost), 2)])

    # Blok 2: kost/resultaat per campagne per periode (voor grafiek 1).
    # Enkel de campagnes die in de laatste periode actief zijn, zodat de grafiek
    # leesbaar blijft ook al bevat de geschiedenis veel oude/gestopte campagnes.
    latest = snaps[-1]
    camp_order = [c["id"] for c in latest["campaigns"]]
    camp_name = {c["id"]: c.get("name", c["id"]) for c in latest["campaigns"]}
    hdr2_row = n + 3
    dat.cell(row=hdr2_row, column=1, value="Periode")
    for j, cid in enumerate(camp_order):
        dat.cell(row=hdr2_row, column=2 + j, value=camp_name[cid])
    for i, snap in enumerate(snaps):
        r = hdr2_row + 1 + i
        dat.cell(row=r, column=1, value=period_label(snap))
        by_id = {c["id"]: c for c in snap["campaigns"]}
        for j, cid in enumerate(camp_order):
            c = by_id.get(cid)
            dat.cell(row=r, column=2 + j,
                     value=(c.get("cost_per_result") if c else None))

    # --- Grafiek 1: kost/resultaat per campagne (lijn, enkel nu actieve campagnes) ---
    m = len(camp_order)
    if m:
        c1 = LineChart()
        c1.title = "Kost per resultaat per campagne (nu actief)"
        c1.y_axis.title = "EUR"
        c1.height, c1.width = 9, 18
        data = Reference(dat, min_col=2, max_col=1 + m, min_row=hdr2_row, max_row=hdr2_row + n)
        cats = Reference(dat, min_col=1, min_row=hdr2_row + 1, max_row=hdr2_row + n)
        c1.add_data(data, titles_from_data=True)
        c1.set_categories(cats)
        ws.add_chart(c1, "B2")

    # --- Grafiek 2: gem. kost/lead accountniveau (lijn) ---
    c2 = LineChart()
    c2.title = "Gem. kost per lead (account)"
    c2.y_axis.title = "EUR"
    c2.height, c2.width = 9, 18
    c2.add_data(Reference(dat, min_col=2, min_row=1, max_row=n + 1), titles_from_data=True)
    c2.set_categories(Reference(dat, min_col=1, min_row=2, max_row=n + 1))
    ws.add_chart(c2, "B22")

    # --- Grafiek 3: spend per dag (kolom) ---
    c3 = BarChart()
    c3.type = "col"
    c3.title = "Spend per dag"
    c3.y_axis.title = "EUR"
    c3.height, c3.width = 9, 18
    c3.add_data(Reference(dat, min_col=3, min_row=1, max_row=n + 1), titles_from_data=True)
    c3.set_categories(Reference(dat, min_col=1, min_row=2, max_row=n + 1))
    ws.add_chart(c3, "B42")

    # --- Grafiek 4: spend resultaat vs boosts (gestapelde kolom) ---
    c4 = BarChart()
    c4.type = "col"
    c4.grouping = "stacked"
    c4.overlap = 100
    c4.title = "Spend: resultaat-campagnes vs boosts"
    c4.y_axis.title = "EUR"
    c4.height, c4.width = 9, 18
    c4.add_data(Reference(dat, min_col=4, max_col=5, min_row=1, max_row=n + 1), titles_from_data=True)
    c4.set_categories(Reference(dat, min_col=1, min_row=2, max_row=n + 1))
    ws.add_chart(c4, "B62")


# ---- tab: Conclusies --------------------------------------------------------
def build_conclusies(wb):
    ws = wb.create_sheet("Conclusies")
    ws.column_dimensions["A"].width = 14
    for col in "BCDEFGH":
        ws.column_dimensions[col].width = 15

    concl = load_conclusies()
    if not concl:
        ws["A1"] = "Nog geen conclusies."
        ws["A1"].font = BOLD
        ws["A2"] = "Vraag na een run om een interpretatie; die komt hier per datum te staan."
        ws["A2"].font = Font(italic=True, color="666666")
        return

    type_fill = {
        "positief": GOOD_FILL,
        "waarschuwing": PatternFill("solid", fgColor="FCE8B2"),
        "actie": PatternFill("solid", fgColor="D2E3FC"),
        "neutraal": PatternFill("solid", fgColor="EDEDED"),
    }
    type_label = {"positief": "Positief", "waarschuwing": "Let op",
                  "actie": "Actie", "neutraal": "Info"}
    top = Alignment(wrap_text=True, vertical="top")

    r = 1
    for item in concl:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
        h = ws.cell(row=r, column=1, value="CONCLUSIE  —  %s   (periode %s t/m %s)" % (
            item.get("date", ""), item.get("period_start", ""), item.get("period_end", "")))
        h.fill = HEADER_FILL
        h.font = HEADER_FONT
        h.alignment = Alignment(vertical="center")
        ws.row_dimensions[r].height = 20
        r += 1

        if item.get("kop"):
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
            c = ws.cell(row=r, column=1, value=item["kop"])
            c.font = Font(bold=True, size=12)
            r += 1

        if item.get("samenvatting"):
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
            c = ws.cell(row=r, column=1, value=item["samenvatting"])
            c.alignment = top
            ws.row_dimensions[r].height = 48
            r += 1

        for p in item.get("punten", []):
            typ = p.get("type", "neutraal")
            lbl = ws.cell(row=r, column=1, value=type_label.get(typ, "Info"))
            lbl.fill = type_fill.get(typ, type_fill["neutraal"])
            lbl.font = BOLD
            lbl.alignment = Alignment(vertical="top", horizontal="center")
            ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=8)
            tc = ws.cell(row=r, column=2, value=p.get("tekst", ""))
            tc.alignment = top
            ws.row_dimensions[r].height = 30
            r += 1

        r += 1  # witruimte tussen conclusies


def main():
    cfg = load_config()
    snaps = load_snapshots()
    wb = Workbook()
    build_snapshots(wb, snaps, cfg)
    build_vergelijking(wb, snaps, cfg)
    build_conclusies(wb)
    build_samenvatting(wb, snaps, cfg)
    build_grafieken(wb, snaps, cfg)

    fname = "%s-mainframe.xlsx" % cfg["klant"].replace(" ", "-")
    out = os.path.join(HERE, "data", fname)
    wb.save(out)
    print("Excel opgeslagen (lokaal): %s" % out)
    print("Weken in geheugen: %d" % len(snaps))

    # Ook naar OneDrive schrijven (auto-sync naar de cloud).
    od = (cfg.get("output") or {}).get("onedrive_dir")
    if od and os.path.isdir(od):
        import shutil
        dest = os.path.join(od, fname)
        shutil.copyfile(out, dest)
        print("Gekopieerd naar OneDrive: %s" % dest)
    elif od:
        print("LET OP: OneDrive-map bestaat niet: %s" % od)

    # Google Drive: de push (en de vraag erom) wordt door de skill afgehandeld,
    # niet hier. build_report.py schrijft enkel lokaal + OneDrive.
    gd = (cfg.get("output") or {}).get("google_drive") or {}
    if gd.get("vraag_elke_run"):
        print("Herinnering: vraag of deze versie naar Google Drive gepusht moet worden.")


if __name__ == "__main__":
    main()
```

## BIJLAGE B — `next_period.py`

```python
# -*- coding: utf-8 -*-
"""
marketing-mainframe :: next_period.py

Kijkt naar de laatste run (meest recente snapshot) en stelt de mogelijke
periodes voor de volgende run voor. Print JSON naar stdout.

Output:
{
  "last_run_end": "2026-06-30" | null,     # week_end van de laatste snapshot
  "today": "2026-07-01",
  "recommended": "since_last_run" | "last_7d",
  "since_last_run": {"since","until","days"} | {"status":"none","reason":...},
  "last_7d": {"since","until","days":7}
}

Gebruik:
  - Handmatige run: toon de opties, laat de gebruiker kiezen
    (sinds laatste run / laatste 7 dagen / andere periode).
  - Automatische run (geen mens): neem altijd "since_last_run"; is dat "none",
    dan zijn er geen nieuwe volledige dagen en stop je.

until = gisteren (vandaag is nog niet af; alleen volledige dagen tellen mee).
"""

import json
import glob
import os
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP_DIR = os.path.join(HERE, "data", "snapshots")


def latest_week_end():
    ends = []
    for fp in glob.glob(os.path.join(SNAP_DIR, "*.json")):
        try:
            with open(fp, encoding="utf-8") as f:
                snap = json.load(f)
            if snap.get("week_end"):
                ends.append(date.fromisoformat(snap["week_end"]))
        except Exception:
            continue
    return max(ends) if ends else None


def main():
    today = date.today()
    until = today - timedelta(days=1)  # gisteren
    last_end = latest_week_end()

    last7 = {
        "since": (until - timedelta(days=6)).isoformat(),
        "until": until.isoformat(),
        "days": 7,
    }

    if last_end is None:
        since_last = dict(last7)  # geen vorige run: eerste venster = 7 dagen
        recommended = "last_7d"
    else:
        since = last_end + timedelta(days=1)
        if since > until:
            since_last = {"status": "none",
                          "reason": "Geen nieuwe volledige dagen sinds de laatste run (%s)." % last_end.isoformat()}
        else:
            since_last = {"since": since.isoformat(), "until": until.isoformat(),
                          "days": (until - since).days + 1}
        recommended = "since_last_run"

    print(json.dumps({
        "last_run_end": last_end.isoformat() if last_end else None,
        "today": today.isoformat(),
        "recommended": recommended,
        "since_last_run": since_last,
        "last_7d": last7,
    }, indent=2))


if __name__ == "__main__":
    main()
```

## BIJLAGE C — `config.json` sjabloon

```json
{
  "klant": "<JOUW KLANTNAAM>",
  "valuta": "EUR",
  "meta_ad_account_id": "<JOUW META AD ACCOUNT ID>",
  "rapport_dag": "maandag",

  "kpis": ["spend", "impressions", "reach", "frequency", "clicks", "ctr", "cpc", "cpm", "results", "cost_per_result", "roas"],

  "type_mapping": {
    "OUTCOME_LEADS": "resultaat-campagne",
    "OUTCOME_SALES": "resultaat-campagne",
    "OUTCOME_APP_PROMOTION": "resultaat-campagne",
    "LINK_CLICKS": "boost/promotie",
    "OUTCOME_TRAFFIC": "boost/promotie",
    "OUTCOME_ENGAGEMENT": "boost/promotie",
    "POST_ENGAGEMENT": "boost/promotie",
    "OUTCOME_AWARENESS": "boost/promotie"
  },
  "type_default": "overig",

  "flags": {
    "cost_per_result_stijging_pct": 20,
    "frequency_max": 3.0
  },

  "roas": {
    "actief": false,
    "opmerking": "Zet op true zodra er aankoopwaarde via je Meta-pixel binnenkomt."
  },

  "output": {
    "lokaal": true,
    "onedrive_dir": "<OPTIONEEL: pad naar een cloud-gesyncte map, of leeg laten>",
    "google_drive": {
      "folder_naam": "Marketing Mainframe - <KLANTNAAM>",
      "folder_id": null,
      "vraag_elke_run": true,
      "auto_push_scheduled": false,
      "bestandsnaam_met_datum": true,
      "opmerking": "Drive-push is optioneel en vraagt na een handmatige run. De koppeling kan niet overschrijven, dus elke push maakt een gedateerd bestand in folder_id."
    }
  },

  "interpretatie": {
    "vraag_elke_run": true,
    "auto_bij_scheduled": true,
    "kaders": "3x-kill-regel, 20%-schaalregel, frequentie <3,0, CTR >=1% en fatigue bij CTR-daling >20%, 70/20/10 (bron: claude-ads van Daniel Agrici).",
    "opmerking": "Handmatige run vraagt om een interpretatie; automatische run genereert ze altijd. Duiding komt op de Conclusies-tab."
  }
}
```

## BIJLAGE D — snapshot-formaat (voorbeeld)

```json
{
  "week_start": "2026-06-22",
  "week_end": "2026-06-28",
  "report_date": "2026-06-28",
  "account": "<KLANTNAAM>",
  "currency": "EUR",
  "campaigns": [
    {
      "id": "1202xxxxxxxxxxxxx",
      "name": "[F1] - Voorbeeld lead-campagne",
      "objective": "OUTCOME_LEADS",
      "spend": 335.60, "impressions": 24411, "reach": 17869, "frequency": 1.37,
      "clicks": 364, "ctr": 1.49, "cpc": 0.92, "cpm": 13.75,
      "results": 10, "result_type": "Leads (form)", "cost_per_result": 33.56, "roas": null
    },
    {
      "id": "1202yyyyyyyyyyyyy",
      "name": "Instagram-bericht: voorbeeld boost",
      "objective": "LINK_CLICKS",
      "spend": 54.02, "impressions": 5995, "reach": 4129, "frequency": 1.45,
      "clicks": 108, "ctr": 1.80, "cpc": 0.50, "cpm": 9.01,
      "results": 113, "result_type": "Link clicks", "cost_per_result": 0.48, "roas": null
    }
  ]
}
```
