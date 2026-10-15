# -*- coding: utf-8 -*-
"""
Genereert MEMBER-SETUP-PROMPT.md uit MEMBER-SETUP-TEMPLATE.md door de placeholders
te vervangen door de echte build_report.py, next_period.py, een generiek config-sjabloon
en een voorbeeld-snapshot.

Template (bron, met @@...@@) en output zijn APARTE bestanden, zodat hergenereren blijft werken.
Draai dit opnieuw telkens build_report.py of next_period.py verandert.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "build_report.py"), encoding="utf-8") as f:
    build_py = f.read().strip()
with open(os.path.join(HERE, "next_period.py"), encoding="utf-8") as f:
    next_py = f.read().strip()

config_template = '''{
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
}'''

snapshot_example = '''{
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
}'''

with open(os.path.join(HERE, "MEMBER-SETUP-TEMPLATE.md"), encoding="utf-8") as f:
    tmpl = f.read()

out = (tmpl
       .replace("@@BUILD_REPORT_PY@@", build_py)
       .replace("@@NEXT_PERIOD_PY@@", next_py)
       .replace("@@CONFIG_TEMPLATE@@", config_template)
       .replace("@@SNAPSHOT_EXAMPLE@@", snapshot_example))

with open(os.path.join(HERE, "MEMBER-SETUP-PROMPT.md"), "w", encoding="utf-8") as f:
    f.write(out)

print("MEMBER-SETUP-PROMPT.md gegenereerd (%d tekens)." % len(out))
