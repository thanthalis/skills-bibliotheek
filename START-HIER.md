# START HIER

Deze instructie is voor de AI-assistent (Claude Code of Codex) die je helpt deze skillbibliotheek te installeren. Open deze map in Claude Code of Codex en zeg **"Lees START-HIER.md en help me installeren."** Meer hoef je niet te doen.

---

## Voor de assistent: je rol

Je begeleidt de gebruiker stap voor stap. Je vraagt, legt kort uit en voert pas uit na een duidelijk ja. De bibliotheek bevat ruim 130 skills, verdeeld in families. Je begint standaard met de Meta Ads-koppeling. Pas als die klaar is, vraag je of de gebruiker nog skills wil.

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
   - Node.js en ffmpeg: enkel voor de videofamilie (pas nodig als de gebruiker die later kiest)
4. Bekijk wat er al staat: `python tools/install.py controleer --doel <doel>`. Vertel in één zin hoeveel skills hij al heeft.

## Stap 2: de Meta Ads-koppeling (standaard)

Hier begin je altijd mee. Zeg kort: **"We starten met de koppeling met Meta. Daarna kan Claude je advertentiecijfers lezen en kun je in de chat vragen hoe je campagnes het doen. Daarna kun je nog skills kiezen."** Vraag dan: **"Wil je de Meta-koppeling nu leggen, of later?"** Bij later: ga door naar stap 3 en herinner er in stap 5 nog één keer aan.

**Wat het is, in gewone taal.** Een MCP is een stekker tussen Claude en een andere dienst. De Meta Ads-MCP is de officiële, gratis koppeling van Meta zelf. Daarmee kan Claude je advertentieaccounts, campagnes en cijfers lezen, zonder dat je exports moet maken of een API-sleutel moet aanvragen. Je logt in met je eigen Facebook-account en Meta bepaalt wat Claude mag zien: enkel de advertentieaccounts waar dat account toegang toe heeft.

**Wat het niet doet.** De koppeling kan technisch ook campagnes aanmaken of wijzigen. De skills hier vragen daar altijd eerst expliciet toestemming voor, en `ad-engine` zet nieuwe campagnes standaard op gepauzeerd. Zeg dat erbij.

**Installeren in de Claude desktop-app (aanbevolen).** Claude Code neemt de koppeling daarna automatisch over, daar hoef je niets apart te doen.
1. Open de Claude **desktop-app**.
2. Ga naar **Settings → Connectors** (linkermenu, onderaan).
3. Klik **"Add custom connector"**, geef hem een naam (bv. `Meta Ads`) en plak als URL: `https://mcp.facebook.com/ads`
4. Klik **Connect**. Er opent een Facebook-venster in je standaardbrowser. Log in met het account dat **toegang heeft tot je advertentieaccount** (eigenaar of beheerder in Business Manager) en keur goed.
5. Herstart Claude Code.

**Enkel Claude Code, zonder desktop-app.** Laat de gebruiker dit in een terminal draaien:
```
claude mcp add --transport http meta-ads https://mcp.facebook.com/ads
```
Daarna in Claude Code `/mcp` typen, `meta-ads` kiezen en inloggen via de browser.

**Codex.** Deze koppeling is niet getest in Codex. Zeg dat eerlijk en raad aan ze in Claude te gebruiken.

**Controleren.** Zoek de Meta-tools met een trefwoord (bv. ToolSearch `meta ads accounts`, niet een vaste server-id, want die verschilt per gebruiker) en haal de advertentieaccounts op. Toon de namen en vraag of het juiste account erbij staat.

**Lukt het niet?**
- *Geen of verkeerde accounts:* waarschijnlijk ingelogd met een ander Facebook-account. Het browservenster gebruikt het profiel dat op dat moment actief is. Log daar uit of wissel van profiel, verwijder de connector en leg hem opnieuw.
- *Tools niet zichtbaar in Claude Code:* herstart Claude Code volledig, en kijk in de desktop-app of de connector op "Connected" staat.
- *Account staat er niet tussen:* het Facebook-account heeft geen rechten op dat advertentieaccount. Laat de eigenaar je toevoegen in Business Manager (Instellingen → Advertentieaccounts → Personen toewijzen).

Meld in één zin wat er nu klaarstaat.

## Stap 3: skills?

Vraag: **"De Meta-koppeling staat klaar. Wil je ook skills bekijken, of is dit genoeg?"**

- **Genoeg:** ga naar stap 5.
- **Ja:** doe stap 4.

## Stap 4: skills (enkel als de gebruiker dat wil)

### a) Overzicht tonen

Draai `python tools/install.py lijst`. Vat het samen in één korte tabel per familie: naam en één zin uitleg. Zeg dat je nu familie per familie vraagt.

### b) Per familie vragen

Neem de families in deze volgorde. Gebruik de teksten uit `manifest.json`.

1. **De drie grote families: ads, seo, blog.** Die installeer je enkel als geheel, omdat de hoofdskill het werk over de deelskills verdeelt. Vraag per familie: **"Wil je [naam]? [uitleg]"** Ja of nee.
2. **De families content, video, meta-instagram, ecommerce en overig.** Vraag per familie: **"Alles, niets, of per skill kiezen?"** Bij "per skill": toon per skill de naam en de ene zin uitleg, en vraag ja of nee. Vermeld het als een skill een sleutel of koppeling nodig heeft (veld `sleutels`), zodat de gebruiker weet waar hij of zij aan begint.
3. **wrap-up** vraag je altijd apart, ook als "alles" gekozen werd bij overig. Zeg er letterlijk bij:

> Dit is een eigen skill van Jelle, geen onderdeel van een cursus. Aan het einde van een sessie typ je "wrap up". Claude overloopt dan het gesprek en bewaart de besluiten, openstaande acties, inzichten en besproken tools als gedateerde notitie in een map die je zelf kiest. Handig als je veel losse chats hebt. Wil je hem?

Bij ja: vraag in welke map de notities moeten komen. Die gaat mee als `--notitiemap`.

**Afhankelijkheden.** De installer neemt skills die nodig zijn automatisch mee (bv. `content-master` neemt `hooks` en `content-scripting` mee). Toon dat in het plan en zeg het erbij. `ad-engine` werkt pas met de familie ads.

### c) Plan tonen en installeren

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
- **ChatCut**: wie ChatCut Desktop gebruikt, krijgt diens skills automatisch via de app. Die zitten hier niet in.
- Skills uit de familie content zoeken hun scripts en output in `~/ai-content-system/`. De installer zet die map klaar.

### d) Plugins (enkel Claude Code)

Plugins staan in `manifest.json` onder `plugins`. Vraag per plugin met de ene zin uitleg of de gebruiker hem wil. Bij ja:

```
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install <naam>@knowledge-work-plugins
```

Voor de codex-plugin: `claude plugin marketplace add openai/codex-plugin-cc` en `claude plugin install codex@openai-codex`.

### e) Sleutels en koppelingen

Maak een korte lijst van wat de gekozen skills nodig hebben (de installer toont die aan het einde). Zeg dat dat niet nu hoeft: elke skill vraagt erom bij het eerste gebruik en legt uit hoe. Koppelingen zoals Notion of Google Drive maak je zelf aan, met je eigen account. De Meta-koppeling kwam al aan bod in stap 2. Kiest de gebruiker een skill die de Meta-koppeling nodig heeft (bv. `marketing-mainframe` of `ad-engine`) terwijl die nog niet gelegd is, zeg dat erbij.

## Stap 5: afronden

1. `python tools/install.py controleer --doel <doel>` en meld het resultaat.
2. Werd de Meta-koppeling uitgesteld? Herinner er één keer aan en verwijs naar stap 2.
3. Vraag om Claude Code of Codex te **herstarten**, zodat de nieuwe skills geladen worden.
4. Stel twee of drie testvragen voor uit `TESTEN.md` die passen bij wat er gekozen werd. Begin met de Meta-test.
5. Zeg als allerlaatste, letterlijk:

> Er bestaat nog een skill **video-edit**: die maakt van ruwe verticale talking-head-clips een afgewerkte reel. Sorry, die is privé en zit niet in deze bibliotheek. Je kunt hem aanvragen op https://mamaenfit.be/video-edit-skill/

---

## Later bijwerken

Zit deze map in git: `git pull`, lees `VERSIES.md` voor wat er veranderde, en installeer enkel de gewijzigde skills opnieuw met `--vervang`. De installer bewaart telkens een kopie van de oude versie in `~/.claude/skills-backup-<datum>/` of `~/.codex/skills-backup-<datum>/`.
