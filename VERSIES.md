# Versies

## 1.0.0 (15 oktober 2026)

Eerste versie. Dezelfde bronversies als Jelles eigen, geteste setup.

| Bron | Versie | Licentie |
|---|---|---|
| AgriciDaniel/claude-ads | v2.0.2 | MIT |
| AgriciDaniel/claude-seo | v2.4.0 | MIT |
| AgriciDaniel/claude-blog | v2.2.0 | MIT |
| coopersimson96/ai-content-system | commit ab7ec3f (na v1.4.0) | Free to use, modify, and share |
| blader/humanizer | v3.1.0 | MIT |
| mvanhorn/last30days-skill | v3.25.0 | MIT |
| teng-lin/notebooklm-py | v0.8.3 (enkel de skill) | MIT |
| vercel-labs/skills (find-skills) | v1.7.0 | MIT |
| thanthalis/video-edit-skill (fork van Tenfold) | commit d3b38f1, opgehaald bij installatie | met toestemming |

Nieuwere versies beschikbaar op 15 oktober: claude-seo v2.4.2, claude-blog v2.3.1, last30days v3.28.0. Nog niet opgenomen, eerst testen.

Aanpassingen bovenop de bronnen, uitgevoerd door de installer:
- `product-demo-video`, `ecommerce-cro`, `shopify-store-design`: kop met naam en beschrijving toegevoegd, anders worden ze niet herkend
- `pdf_generator.py`: lettertypes naast het script in plaats van in `~/Library/Fonts`, zodat het ook op Windows werkt
- Codex: paden `~/.claude/skills` en `~/.claude/content-system` worden `~/.codex/...`

Niet opgenomen: persoonlijke skills van Jelle (second brain, Zoom-sync, eigen merk en klanten), carousel-gen (vervangen door carousel-builder), en de skills van ChatCut (komen met de app).

## Een update voorbereiden (voor wie de bibliotheek beheert)

1. In `tools/vendor_sources.py` de `ref` van de bron verhogen (video-edit: in `manifest.json`)
2. `py tools/vendor_sources.py <bron>`
3. De betrokken skills testen
4. Hier een nieuwe versie noteren, met wat er veranderde
5. `py tools/scan_secrets.py`, dan committen
