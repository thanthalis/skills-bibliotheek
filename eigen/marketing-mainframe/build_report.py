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
