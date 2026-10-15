---
name: marketing-mainframe
description: Wekelijkse meta-analyse van Meta-advertenties (campagnes en boosts/reels) per klant. Haalt de laatste 7 dagen op uit het gekoppelde Meta-ad-account, voegt een gedateerde snapshot toe aan een meegroeiend Excel-geheugen, en herbouwt de vergelijking week-na-week. Draagbaar per klant via config.json. Trigger op "marketing mainframe", "wekelijkse adsanalyse", "weekrapport meta", "campagne-overzicht".
---

# Marketing Mainframe

Een draagbaar wekelijks rapportsysteem voor Meta-advertenties. Per klant één map met
`config.json` en een meegroeiend Excel-bestand. De Excel is het geheugen; de losse
weeksnapshots in `data/snapshots/*.json` zijn de bron van waarheid (verwijder die nooit).

## Mapstructuur

```
marketing-mainframe/
  config.json                  <- enige bestand dat per klant verschilt
  build_report.py              <- bouwt de Excel uit de snapshots
  SKILL.md
  data/
    <Klant>-mainframe.xlsx      <- het geheugen, 3 tabbladen
    snapshots/
      YYYY-MM-DD.json           <- 1 bestand per wekelijkse run
```

## Eerste keer

Staat er in `config.json` nog `<JOUW KLANTNAAM>` of `<JOUW META AD ACCOUNT ID>`, vraag die dan eerst aan de gebruiker en vul ze in. `onedrive_dir` en de Google Drive-map zijn optioneel: laat ze leeg als de gebruiker ze niet wil. Nodig: een koppeling met Meta Ads (de Meta Ads-connector of -MCP) en het Python-pakket `openpyxl`. Wil iemand het rapport zonder Claude Code opzetten, dan staat alles in `MEMBER-SETUP-PROMPT.md`.

## Wekelijkse run (dit doet de skill)

1. **Lees `config.json`** in dezelfde map. Hieruit komt het `meta_ad_account_id`,
   de KPI-lijst, de `type_mapping` (doel -> campagne/boost) en de `flags`.

2. **Bepaal de periode** met `python next_period.py`. Dat toont wanneer de laatste run
   was en twee vensters (`since_last_run` en `last_7d`), plus welke aanbevolen is.
   - **Handmatige run:** leg de keuze voor aan de gebruiker en wacht op antwoord:
     (a) **Sinds de laatste run** (X dagen) - aanbevolen, sluit naadloos aan zonder overlap;
     (b) **Enkel de laatste 7 dagen** - let op: kan overlappen met de vorige periode;
     (c) **Andere periode** - vraag een eigen `since`/`until`.
     Is `since_last_run` gelijk aan `{"status":"none"}`, meld dat er sinds de laatste run
     geen nieuwe volledige dagen zijn en bied (b) of (c) aan.
   - **Automatische run (geplande taak, geen mens):** kies altijd `since_last_run`. Is dat
     `none`, stop dan en meld dat er niets nieuws is (schrijf geen snapshot).

   Haal de gekozen periode op uit het Meta-ad-account via de Ads-MCP, op campagne-niveau,
   met twee aanroepen van `ads_get_ad_entities` (account = `meta_ad_account_id`,
   `time_range: {since, until}`, `level: "campaign"`, `sort: "spend_descending"`):
   - aanroep A, velden: `id, name, objective, spend, impressions, reach, frequency, clicks, ctr, cpc, cpm`
   - aanroep B, velden: `id, name, results, cost_per_result`
   Voeg beide samen op `id`.

3. **Normaliseer naar ruwe getallen.** De MCP geeft geformatteerde strings terug
   (bv. `"€ 335,60 EUR"`, `"24.411"`, `"1,49%"`, `results.value = "10 (Leads (form))"`).
   Zet om naar floats/ints (Europese notatie: punt = duizendtal, komma = decimaal).
   Splits bij `results`/`cost_per_result` de waarde van het label: het label gaat naar
   `result_type`, het getal naar `results` / `cost_per_result`. Geen resultaten in de
   periode -> `results: 0`, `cost_per_result: null`.

4. **Schrijf de snapshot** naar `data/snapshots/YYYY-MM-DD.json` (datum = rapportdag),
   met `week_start` (=since), `week_end` (=until), `report_date`, `account`, `currency`
   en de lijst `campaigns` (zelfde velden als de bestaande snapshot als voorbeeld).

5. **Draai `python build_report.py`.** Dit herbouwt de drie tabbladen uit alle
   snapshots en schrijft de Excel lokaal én naar `output.onedrive_dir` (auto-sync
   naar de cloud). Het overschrijft nooit data.

6. **Deel-kanaal.** OneDrive (`output.onedrive_dir`) is altijd het stabiele, verse
   deel-kanaal: zelfde pad, elke run overschreven.

7. **Rapporteer kort aan de gebruiker**: periode + aantal dagen, totale spend, aantal
   leads en gem. kost/lead (resultaat-campagnes), de boosts apart, en alles wat geflagd
   is. Vermeld de week-na-week-verandering in kost per resultaat.

8. **Google Drive-push (vraag na de run).** De Google Drive MCP kan een bestaand
   bestand NIET in-place bijwerken (geen update/delete-tool), dus elke push wordt een
   gedateerd bestand `<klant>-mainframe-<week_end>.xlsx` in `output.google_drive.folder_id`
   (een versie-archief, geen duplicaat met dezelfde naam).
   - **Handmatige run:** als `output.google_drive.vraag_elke_run` true is, vraag dan:
     "Wil je deze versie ook naar Google Drive pushen? (ja / nee)". Bij ja: base64-encodeer
     de verse xlsx en maak het gedateerde bestand aan in `folder_id` via de Drive MCP, en
     geef de deel-link terug. Bij nee: sla over.
   - **Automatische run (geplande taak):** push enkel als
     `output.google_drive.auto_push_scheduled` true is; anders overslaan.

9. **Interpretatie (vraag na de Drive-vraag).** Duiding van de cijfers, gebaseerd op de
   kaders in `interpretatie.kaders` (de claude-ads skills van Daniel Agrici): 3x-kill-regel,
   20%-schaalregel, frequentie <3,0, CTR ≥1% en fatigue bij CTR-daling >20%, en 70/20/10.
   - **Handmatige run:** als `interpretatie.vraag_elke_run` true is, vraag: "Wil je een
     interpretatie van de resultaten?". Bij ja: analyseer de laatste periode volgens die
     kaders, **toon de duiding in chat**, én schrijf ze naar
     `data/conclusies/<rapportdatum>.json` met velden `date, period_start, period_end,
     kop, samenvatting, punten` (elk punt = `{type, tekst}`, type =
     positief | waarschuwing | actie | neutraal). Draai daarna opnieuw
     `python build_report.py` zodat de Conclusies-tab de duiding toont.
   - **Automatische run:** als `interpretatie.auto_bij_scheduled` true is, genereer de
     interpretatie altijd (zonder vragen), schrijf ze weg en herbouw.

## De tabbladen

- **Snapshots** — ruwe geschiedenis, 1 rij per (periode, campagne). Lead-campagnes en
  boosts zijn gekleurd via de `Type`-kolom. Groeit elke run aan.
- **Vergelijking** — de laatste periode per campagne: spend, resultaten, kost/resultaat,
  status (nieuw/actief), vorige periode, delta %, gemiddelde laatste 4, vlag. Plus een
  blok "Gestopt sinds vorige periode". Dit is het werkblad.
- **Conclusies** — de duiding per datum (uit `data/conclusies/*.json`), met
  Positief / Let op / Actie / Info. Nieuwste bovenaan.
- **Samenvatting** — 1 rij per periode op accountniveau: dagen, totale spend, spend/dag,
  resultaat-campagnes vs boosts gesplitst, leads en gem. kost/lead.
- **Grafieken** — vier trendgrafieken die meegroeien (kost/resultaat per actieve campagne,
  gem. kost/lead, spend/dag, spend resultaat vs boosts).

## Onderscheid campagne vs boost/reel

Bepaald door het campagnedoel (`objective`) via `type_mapping` in de config.
`OUTCOME_LEADS`/`OUTCOME_SALES` -> resultaat-campagne; `LINK_CLICKS`/`OUTCOME_TRAFFIC`/
`OUTCOME_ENGAGEMENT` -> boost/promotie. Pas de mapping aan per klant indien nodig.

## ROAS

Standaard uit (`roas.actief: false`): de echte klantwaarde komt niet via de pixel
binnen, dus de kolom blijft leeg om geen vals getal te tonen. Zet aan zodra er wel
aankoopwaarde doorkomt.

## Nieuwe klant toevoegen (draagbaar maken)

Kopieer de hele map, vervang `config.json` (nieuw `meta_ad_account_id`, klantnaam,
eventueel andere `type_mapping`/`flags`), leeg `data/snapshots/`, en draai de
wekelijkse run. Verder niets aan te passen.
