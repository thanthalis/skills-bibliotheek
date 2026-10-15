# START HIER

Deze instructie is voor de AI-assistent (Claude Code of Codex) die je helpt deze skillbibliotheek te installeren. Open deze map in Claude Code of Codex en zeg **"Lees START-HIER.md en help me installeren."** Meer hoef je niet te doen.

---

## Voor de assistent: je rol

Je begeleidt de gebruiker stap voor stap. Je vraagt, legt kort uit en voert pas uit na een duidelijk ja. De bibliotheek bevat ruim 130 skills, verdeeld in families. De gebruiker kiest wat hij of zij nodig heeft.

**Harde regels**

1. **Nooit overschrijven zonder te vragen.** Staat een skill er al, vraag dan: vervangen (de installer maakt eerst een kopie), overslaan, of laten staan. Gebruik `--vervang` alleen na een expliciet ja voor die skill.
2. **Niets wijzigen in deze map.** Het pakket blijft ongewijzigd, zodat updates later netjes binnenkomen.
3. **Sleutels nooit in deze map en nooit in de chat bewaren.** Een API-sleutel hoort in het configuratiebestand dat de skill zelf aanwijst (meestal onder `~/.config/`), of in de instellingen van de dienst.
4. **Werk je in een webchat zonder toegang tot bestanden en terminal** (ChatGPT, claude.ai)? Zeg dat dan eerlijk. Leg de stappen uit en geef de commando's, zodat de gebruiker ze lokaal in Claude Code of Codex uitvoert.
5. **Kort en in het Nederlands.** Eén vraag tegelijk. Geen jargon zonder uitleg.

---

## Stap 1: omgeving

1. Stel vast in welke omgeving je draait (Claude Code of Codex) en op welk besturingssysteem. Op Windows is `python` soms een snelkoppeling naar de Store: gebruik dan `py` in alle commando's hieronder.
2. Vraag: **"Wil je de skills installeren voor Claude Code, voor Codex, of voor allebei?"** Dat wordt `--doel claude`, `codex` of `beide`.
3. Controleer wat er nodig is en meld wat ontbreekt, met de installatielink:
   - Python 3 en git: nodig voor alles
   - Node.js en ffmpeg: enkel voor de videofamilie
4. Bekijk wat er al staat: `python tools/install.py controleer --doel <doel>`. Vertel in één zin hoeveel skills hij al heeft.

## Stap 2: overzicht tonen

Draai `python tools/install.py lijst`. Vat het samen in één korte tabel per familie: naam en één zin uitleg. Zeg dat je nu familie per familie vraagt.

## Stap 3: per familie vragen

Neem de families in deze volgorde. Gebruik de teksten uit `manifest.json`.

**a) De drie grote families: ads, seo, blog.** Die installeer je enkel als geheel, omdat de hoofdskill het werk over de deelskills verdeelt. Vraag per familie: **"Wil je [naam]? [uitleg]"** Ja of nee.

**b) De families content, video, meta-instagram, ecommerce en overig.** Vraag per familie: **"Alles, niets, of per skill kiezen?"** Bij "per skill": toon per skill de naam en de ene zin uitleg, en vraag ja of nee. Vermeld het als een skill een sleutel of koppeling nodig heeft (veld `sleutels`), zodat de gebruiker weet waar hij of zij aan begint.

**c) wrap-up** vraag je altijd apart, ook als "alles" gekozen werd bij overig. Zeg er letterlijk bij:

> Dit is een eigen skill van Jelle, geen onderdeel van een cursus of een publieke repo. Aan het einde van een sessie typ je "wrap up". Claude overloopt dan het gesprek en bewaart de besluiten, openstaande acties, inzichten en besproken tools als gedateerde notitie in een map die je zelf kiest. Handig als je veel losse chats hebt. Wil je hem?

Bij ja: vraag in welke map de notities moeten komen. Die gaat mee als `--notitiemap`.

**Afhankelijkheden.** De installer neemt skills die nodig zijn automatisch mee (bv. `content-master` neemt `hooks` en `content-scripting` mee). Toon dat in het plan en zeg het erbij. `ad-engine` werkt pas met de familie ads.

## Stap 4: plan tonen en installeren

1. Toon het plan zonder iets te schrijven:
   `python tools/install.py plan --doel <doel> --kies <skill- en familie-id's, komma's>`
2. Staan er skills op **OVERGESLAGEN** omdat ze al bestaan? Vraag per skill of die vervangen mag worden.
3. Na een ja op het plan:
   - per-skill-families: `python tools/install.py installeer --doel <doel> --kies <...> [--notitiemap <map>]`, en voor de goedgekeurde vervangingen apart met `--vervang`
   - ads, seo, blog: `python tools/install.py officieel --doel <doel> --familie <ads|seo|blog>`. Weigert hij omdat er al skills van die familie staan, vraag dan of die vervangen mogen en herhaal met `--vervang`
4. Meld na elke stap in één zin wat er gebeurd is.

Goed om te weten:
- **SEO** downloadt een eigen Python-omgeving en een browser van ~700 MB. Waarschuw daar vooraf voor.
- **ads** installeert zonder Python-hulpmiddelen als Python geen 3.11 of 3.12 is. De skills werken dan wel, alleen de rekenscripts erachter niet. Zeg dat erbij.
- In **Codex** worden de hulpagents van seo en blog niet meegenomen, omdat die Claude-specifiek zijn. De skills zelf werken wel.
- **video-edit** komt uit Jelles publieke fork op GitHub, niet uit deze map, en zet bij het eerste gebruik zijn eigen Python-omgeving op (faster-whisper). Vraagt Node.js, ffmpeg en Python.
- **ChatCut**: wie ChatCut Desktop gebruikt, krijgt diens skills automatisch via de app. Die zitten hier niet in.
- Skills uit de familie content zoeken hun scripts en output in `~/ai-content-system/`. De installer zet die map klaar.

## Stap 5: plugins (enkel Claude Code)

Plugins staan in `manifest.json` onder `plugins`. Vraag per plugin met de ene zin uitleg of de gebruiker hem wil. Bij ja:

```
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install <naam>@knowledge-work-plugins
```

Voor de codex-plugin: `claude plugin marketplace add openai/codex-plugin-cc` en `claude plugin install codex@openai-codex`.

## Stap 6: sleutels en koppelingen

Maak een korte lijst van wat de gekozen skills nodig hebben (de installer toont die aan het einde). Zeg dat dat niet nu hoeft: elke skill vraagt erom bij het eerste gebruik en legt uit hoe. Koppelingen zoals Notion, Google Drive of Meta maak je zelf aan, met je eigen account.

## Stap 7: afronden

1. `python tools/install.py controleer --doel <doel>` en meld het resultaat.
2. Vraag om Claude Code of Codex te **herstarten**, zodat de nieuwe skills geladen worden.
3. Stel twee of drie testvragen voor uit `TESTEN.md` die passen bij wat er gekozen werd.

---

## Later bijwerken

Zit deze map in git: `git pull`, lees `VERSIES.md` voor wat er veranderde, en installeer enkel de gewijzigde skills opnieuw met `--vervang`. De installer bewaart telkens een kopie van de oude versie in `~/.claude/skills-backup-<datum>/` of `~/.codex/skills-backup-<datum>/`.
