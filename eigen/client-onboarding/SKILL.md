---
name: client-onboarding
description: Volledig geautomatiseerde onboarding voor een nieuwe klant. Doorloopt alle 7 stappen van de Client Content System Workflow in één sessie — intake, marktonderzoek, lead magnet, scripts, e-mailreeks, Notion hub en infrastructuurchecklist.
argument-hint: "onboarding voor klant-x" or "nieuwe klant: klant-y"
context: conversation
---

# Client Onboarding — Volledig Geautomatiseerd

Eén commando. Één sessie. Volledige content-infrastructuur voor een nieuwe klant.

Na de intake (10 vragen, ~5 minuten) loopt alles automatisch door: marktonderzoek, lead magnet, Vercel deploy, 12 Reel scripts, e-mailreeks en een complete Notion Marketing Hub.

---

## STAP 1 — Intake (enige manuele stap)

Stel deze vragen **één voor één** aan de gebruiker. Wacht op elk antwoord voor je verdergaat.

1. **Klantnaam** (voor bestandsnamen, bv. "klant-x" of "klant-y")?
2. **Website URL?**
3. **Type business?** (B2B coaching / B2C product / e-commerce / lokale dienst / ...)
4. **Doelgroep** — beschrijf: leeftijd, profiel, pijnpunt, verlangen
5. **Aanbod** — naam van het product/dienst, prijs excl. BTW, prijs incl. BTW
6. **Extra tools/kosten voor de klant na aankoop?** (bv. GoHighLevel €200/m, Mailchimp, ...)
7. **Toon en schrijfstijl?** (direct / warm / inspirerend / zakelijk / ...)
8. **Sociale platforms?** (Instagram, Facebook, LinkedIn, TikTok, ...)
9. **Community aanwezig of gepland?** (ja/nee, welk platform?)
10. **Zijn er bestaande content-assets?** (logo, kleuren, slogan, ...)

Sla alle antwoorden op als:
`~/content-output/[slug]/CONTEXT.md`

### CONTEXT.md structuur

```markdown
# [Klantnaam] — Merkcontext

## Business
- Type: ...
- Website: ...
- Aanbod: ... (€... excl. / €... incl. BTW)
- Extra tools: ...

## Doelgroep
- Profiel: ...
- Pijnpunt: ...
- Verlangen: ...

## Communicatie
- Toon: ...
- Platforms: ...
- Community: ...

## Assets
- ...
```

Bevestig aan de gebruiker: **"Merkcontext opgeslagen. Start nu automatisch met stap 2..."**

---

## STAP 2 — Marktonderzoek

Voer automatisch uit: `/last30days`

**Instructies:**
- Gebruik `CONTEXT.md` als input — lees de niche, doelgroep en platforms
- Kies automatisch de 3 meest relevante topics op basis van de niche
- Geen goedkeuring vragen — kies zelf de beste topics
- Sla output op als: `~/content-output/[slug]/last30days.md`

Na afronding: **"Marktonderzoek klaar. Start stap 3..."**

---

## STAP 3 — Lead Magnet + Landing Page

Voer automatisch uit: `/hand-raiser`

**Instructies:**
- Gebruik `CONTEXT.md` + `last30days.md` als input
- Genereer een lead magnet passend bij de niche en doelgroep
- Maak de bijhorende landingspagina aan
- Deploy automatisch naar Vercel (repo: thanthalis/lead-pages)
- Live URL: https://lead-pages-liart.vercel.app

**Output:**
- PDF opgeslagen in `~/content-output/[slug]/lead-magnet.pdf`
- Landingspagina gedeployed, URL opslaan in `CONTEXT.md`

Na afronding: **"Lead magnet live. Start stap 4..."**

---

## STAP 4 — Contentkalender + Scripts + Pipeline

Voer automatisch en **zonder te pauzeren** uit in deze volgorde:

### 4a — Scripts via `/content-master`
**Instructies:**
- Gebruik `CONTEXT.md` + `last30days.md` als input
- Genereer een contentkalender voor 3 weken vooruit
- Schrijf 12 Reel scripts, gegroepeerd in 4 series van 3
- Elke serie heeft een eigen hook-stijl en call-to-action
- Sla op als: `~/content-output/[slug]/[slug]-scripts-batch1.md`

**Push-to-production pipeline (automatisch, geen goedkeuring vragen):**
- Hand Raiser PDF genereren per script
- PDF uploaden naar Google Drive
- Vercel landingspagina aanmaken per script
- Notion script-pagina's aanmaken (alle 12) als **subpagina's onder de Content Master pagina van de klant hub** (NIET in de algemene Script Library):
  - Parent: de Content Master subpagina onder `[Klantnaam] — Marketing Hub`
  - Elk script als aparte subpagina met **volledige scriptinhoud**:
    - Hooks (A, B, C) met aanduiding van type en [FACE]/[BROLL]
    - Volledig script (Hook A versie), regel per regel
    - Caption (klaar om te kopiëren)
    - Text overlays met tijdscodes
    - Production notes (waarom het werkt + filmtips)
  - **Geen Windows-paden als links** — enkel publieke URLs (Vercel, Google Drive, website van de klant)

### 4b — Pipeline via `/content-pipeline` (direct na 4a, geen pauze)
**Instructies:**
- Laad `[slug]-scripts-batch1.md` als input
- Maak een posting kalender aan voor de 3 weken vooruit
- Stel post-datums in per script op basis van de contentkalender uit 4a
- Wijs elke script toe aan de juiste dag in de pipeline
- Geen goedkeuring vragen — gebruik de datums uit de contentkalender

Na afronding van 4a én 4b: **"Scripts + pipeline klaar. Start automatisch stap 5..."**

---

## STAP 5 — E-mailreeks

Voer **automatisch** uit direct na stap 4 — geen pauze, geen goedkeuring vragen.

Voer uit: schrijf de e-mailreeks zelf (geen aparte skill nodig).

**Instructies:**
- Gebruik `CONTEXT.md` als input
- Schrijf een reeks van 4 mails:
  1. **Welkomstmail** — lead magnet leveren + verwachtingen stellen
  2. **Nurture mail** — waarde geven, probleem verdiepen
  3. **Aankondiging** — aanbod introduceren
  4. **Lancering** — aanbod met CTA en deadline
- Toon matcht de schrijfstijl uit `CONTEXT.md`
- Elke mail: onderwerpregel, preheader, volledige body, CTA-knop tekst
- Sla op als: `~/content-output/[slug]/email-reeks.md`

Na afronding: **"E-mailreeks klaar. Start stap 6..."**

---

## STAP 6 — Notion Marketing Hub aanmaken

Maak automatisch aan via **Notion MCP**.

**Paginastructuur:**
```
[Klantnaam] — Marketing Hub
├── Marketing Plan (NL)
├── Lead Magnet
├── E-mail Reeks
└── Content Master
```

**Vul in per pagina:**
- **Marketing Plan:** merkidentiteit, doelgroep, aanbod + prijzen, kanaalstrategie
- **Lead Magnet:** URL van de live landingspagina, PDF link, beschrijving van het aanbod
- **E-mail Reeks:** de 4 mails volledig uitgeschreven
- **Content Master:** volledige contentkalender + alle 12 scripts

Notion config: `~/.config/notion-content/config.json`
Parent database: Content Production Hub (`3327c75802cc81948686f989684c0936`)

Na afronding: **"Notion Marketing Hub aangemaakt. Start stap 7..."**

---

## STAP 7 — Infrastructuur checklist + samenvatting

Toon een overzicht van alles wat gedaan is en wat nog open staat.

**Gedaan in deze sessie:**
- [x] Merkcontext (CONTEXT.md)
- [x] Marktonderzoek (last30days.md)
- [x] Lead Magnet + Vercel landing page
- [x] 12 Reel scripts in 4 series
- [x] E-mailreeks (4 mails)
- [x] Notion Marketing Hub

**Nog te doen door klant of jou:**
- [ ] Google Drive koppeling controleren (`/gdocs-setup`)
- [ ] E-mailplatform instellen (Brevo, Mailchimp of Beehiiv)
- [ ] Prijzen/details producten aanvullen op website
- [ ] Instagram bio updaten met lead magnet CTA
- [ ] Community aanmaken indien gewenst (Facebook of Skool)
- [ ] Vercel URL doorgeven aan klant

**Output bestanden:**
```
~/content-output/[slug]/
├── CONTEXT.md
├── last30days.md
├── lead-magnet.pdf
├── [slug]-scripts-batch1.md
└── email-reeks.md
```

Sluit af met: **"Onboarding volledig klaar voor [Klantnaam]. Nieuwe Claude Code sessie starten voor de volgende klant om context drift te vermijden."**

---

## Vaste regels (nooit overslaan)

- **Merkcontext altijd eerst** — scripts zonder CONTEXT.md worden generiek
- **Vercel deploy = publieke URL**, altijd reviewen voor je deelt met klant
- **Elke klant krijgt een eigen subfolder** onder `/output/[slug]/`
- **Nieuwe Claude Code sessie starten per klant**
- **Paden:** gebruik `~/content-output/[slug]/`. Op Windows is `~` je gebruikersmap.
- **Scripts staan volledig uitgeschreven in Notion** — hooks, volledig script, caption, text overlays en production notes per pagina. Geen verwijzingen naar lokale bestanden.
- **Geen Windows-paden als links in Notion** — gebruik enkel publieke URLs: Vercel-pagina's, Google Drive-links, of de website van de klant. Een pad zoals `C:\Users\...` heeft geen betekenis buiten deze machine.
