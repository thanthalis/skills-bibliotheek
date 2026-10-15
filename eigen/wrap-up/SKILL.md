---
name: wrap-up
description: >
  Sessie wrap-up aan het einde van een werksessie. Trigger wanneer de gebruiker
  "/wrap up", "/wrapup", "wrap up", "sessie afsluiten" of "sla de sessie op" typt.
  Scant de volledige conversatie, haalt besluiten, actiepunten, inzichten, context
  over mensen, klanten en projecten, en besproken tools eruit, en bewaart dat als
  YYYY-MM-DD-sessie.md in de notitiemap van de gebruiker.
---

# /wrap up: sessie wrap-up

Doel: geen waardevolle informatie laten liggen. Elke sessie levert een korte, doorzoekbare notitie op.

## Instelling

De notitiemap staat hieronder. Bij de installatie is die ingevuld; staat er nog `<<NOTITIEMAP>>`, vraag de gebruiker dan eenmalig waar sessienotities moeten komen en stel voor die regel hier aan te passen.

```
NOTITIEMAP = <<NOTITIEMAP>>
```

## Stap 1: scan de volledige sessie

Loop de hele conversatie terug en haal per categorie eruit wat er echt besproken werd. Verzin niets. Laat een sectie leeg als er niets relevants was.

**Besluiten**
Afgeronde keuzes, geen twijfels of open vragen. Formuleer als feit: "X wordt Y" of "Er is gekozen voor Z."

**Actiepunten**
Taken die uit de sessie volgen, in dit formaat:
`- [ ] [eigenaar] Wat er moet gebeuren (deadline: X)`
Laat eigenaar of deadline weg als ze niet vermeld werden. Concreet en uitvoerbaar: niet "nadenken over X" maar "X opzoeken", "X bouwen", "X sturen".

**Inzichten en learnings**
Concepten of lessen die later herbruikbaar zijn. Kennisopbouw, geen to-do.

**Context: mensen, klanten, projecten**
Nieuwe of bijgewerkte feiten over de gebruiker, collega's, partners, klanten en lopende projecten. Noteer ook als eerder bekende info gecorrigeerd werd.

**Tools en systemen**
Alles wat gebouwd, ingesteld of besproken werd: workflows, advertentie-instellingen, scripts, integraties, automatiseringen. Genoeg detail om het later op te pikken.

## Stap 2: maak het bestand aan

Bepaal de datum van vandaag (YYYY-MM-DD). Vul de template in. Schrijf bij een lege sectie expliciet: _"Geen [besluiten/actiepunten/...] deze sessie."_

Sla op als `NOTITIEMAP/YYYY-MM-DD-sessie.md`. Bestaat dat bestand al, voeg dan `-2`, `-3` toe. Zonder schrijftoegang: toon de volledige inhoud zodat de gebruiker hem kan kopiëren.

```markdown
# Sessie YYYY-MM-DD

## Besluiten
-

## Actiepunten
- [ ]

## Inzichten en learnings
-

## Context: mensen, klanten, projecten
-

## Tools en systemen
-

---
_Gegenereerd op YYYY-MM-DD met /wrap up_
```

## Stap 3: bevestig

```
Sessie opgeslagen als NOTITIEMAP/YYYY-MM-DD-sessie.md
```

Vermeld daarna in één zin de belangrijkste openstaande actie.

## Kwaliteitscheck voor je opslaat

- Is elke sectie ingevuld of expliciet leeg gelaten?
- Zijn de actiepunten concreet genoeg om meteen uit te voeren?
- Is de context specifiek genoeg voor later?
- Klopt de bestandsnaam (YYYY-MM-DD-sessie.md)?
- Staat er niets in dat niet in de sessie besproken werd?

_Oorspronkelijk gemaakt door Jelle Eeckhaut als persoonlijke skill; dit is de neutrale versie._
