# Testvragen na de installatie

Herstart eerst Claude Code of Codex. Kies er twee of drie die passen bij wat je installeerde.

| Familie | Vraag | Wat je zou moeten zien |
|---|---|---|
| Meta-koppeling | "Toon mijn Meta-advertentieaccounts" | de namen van de advertentieaccounts waar je Facebook-account toegang toe heeft |
| meta-instagram | "Maak het weekrapport meta" (marketing-mainframe) | eerst vragen naar klantnaam en advertentieaccount, daarna een Excel-rapport van de laatste 7 dagen |
| ads | "Welke vijf dingen zou je nakijken in een Google Ads-account met €13 per dag en drie campagnes?" | een concrete checklist, zonder dat hij iets in een account wijzigt |
| ads | `/ads math` "Wat mag een lead kosten bij €2.000 omzet per klant, 50% marge en 20% sluiting?" | €200 waarde per lead, met een doelkost per lead |
| seo | `/seo page https://jouwsite.be/een-pagina` | een analyse van één pagina met prioriteiten |
| blog | "Maak een blogbrief over [een onderwerp uit jouw vak]" | een brief met zoekwoord, opbouw en woordaantallen |
| content | `/hooks` "Tien hooks voor een reel over [jouw onderwerp]" | tien openingszinnen met het gebruikte framework |
| video | "Maak een titelkaart van vijf seconden met de tekst 'Make moments matter'" (vraagt Node.js) | een Hyperframes-project met een voorbeeld |
| overig | "Haal de AI-taal uit deze tekst: [plak een alinea]" (humanizer) | dezelfde inhoud, natuurlijker geschreven |
| overig | "wrap up" aan het einde van een gesprek | een notitie in je gekozen map |

Werkt een skill niet: vraag de assistent "Waarom werd skill X niet gebruikt?" en draai `python tools/install.py controleer --doel claude` (of `codex`).
