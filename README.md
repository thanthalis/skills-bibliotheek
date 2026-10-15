# Skillbibliotheek

De skills waarmee Jelle werkt in Claude Code en Codex, voor vrienden en oud-klanten. Ruim 130 skills voor advertenties, SEO, blogs, content, video, webshops en algemeen werk, met een begeleide installatie.

**Installeren:** download of clone deze map, open hem in Claude Code of Codex en zeg: *"Lees START-HIER.md en help me installeren."* Je assistent legt per familie en per skill uit wat ze doet en vraagt of je ze wil. Er wordt niets overschreven zonder dat je het bevestigt.

## Wat erin zit

| Map | Wat |
|---|---|
| `START-HIER.md` | de instructie waarmee je assistent je door de installatie leidt |
| `manifest.json` | alle families en skills, met uitleg, afhankelijkheden en benodigde sleutels |
| `TESTEN.md` | testvragen na de installatie |
| `VERSIES.md` | welke versie van elke bron, en wat er veranderde |
| `vendor/` | ongewijzigde momentopnames van de bronnen, met licentie en `BRON.md` |
| `eigen/` | skills van Jelle: client-onboarding, kling-ai, wrap-up |
| `patches/` | lettertypes voor de pdf-generator (Google Fonts, OFL) |
| `tools/install.py` | de installer (Claude Code en Codex) |
| `tools/vendor_sources.py` | haalt nieuwe versies van de bronnen op, voor updates |
| `tools/scan_secrets.py` | controleert dat er geen sleutels of mailadressen in de map staan |

## Bijwerken

`git pull` in deze map, lees `VERSIES.md`, en vraag je assistent de gewijzigde skills opnieuw te installeren.

## Wat je zelf nog regelt

Sleutels en koppelingen (Notion, Google Drive, Meta, API-sleutels) maak je aan met je eigen accounts. De skills vragen erom bij het eerste gebruik. Deze map bevat geen sleutels of persoonlijke gegevens van Jelle.

## Licenties

claude-ads, claude-seo, claude-blog, humanizer, last30days, notebooklm-py en vercel-labs/skills zijn MIT. Coopers AI Content System is "Free to use, modify, and share". video-edit is een fork van Tenfold (`tenfoldmarc/video-edit-skill`), gedeeld met toestemming, en wordt bij de installatie rechtstreeks uit die fork gehaald. De licentie van elke bron staat in zijn map onder `vendor/`. De lettertypes in `patches/fonts` zijn Google Fonts onder de SIL Open Font License.
