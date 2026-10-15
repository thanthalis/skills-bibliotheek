# Changelog

All notable changes to the AI Content System will be documented in this file.

## [1.4.0] - 2026-06-25

### Added
- **`ad-engine`** - The 1-Prompt Meta Ads Engine. Asks 4 discovery questions, then runs an end-to-end pipeline: competitor intel (`/ads competitor`), brand-site scraping for palette/type/voice, bulk image-to-image generation (kie.ai gpt-image-2), paired ad copy (`/ads creative`), and a PAUSED Meta campaign via the Meta Ads MCP. Dynamic Product Ad principles (variant matrix + brand compliance) are applied inline. Saves reusable brand profiles for one-command re-runs. Ships with `templates/brand-profile.template.json`, a `brands/` README + example profile, and a pre-flight tool check. Always creates campaigns PAUSED — never auto-launches spend.

### Improved
- **`hooks`** - Added the high-performing **Cost / Service-Kill + Free + Timeframe** pattern (with an authenticity requirement) and the **Cadence-Match 4-beat hook structure** (consequence opener → free-scoop → "so now you can" payoff → "let me show you"), the beat most run-on hooks are missing.
- **`hand-raiser`** - Added the **Tool-Demo Hand-Raiser Architecture**: a fixed 00→04 narrative arc (Real Problem → Install → Use it → Receipts → The part most people miss), two bookending honesty boxes (attribution + when-to-skip) as a trust move, and section-type discipline for tool/repo/skill handouts.
- **`carousel-builder`** - Added an **Advanced quality techniques** section: headlines-carry-the-whole-story-as-one-conversational-thread (the #1 lever), pull-the-skin-from-the-funnel's-assets, one recurring artifact that literally depicts the promise (built at two scales), headline-dominant covers, motion-synced highlights, single self-evident CTA bundles, and a freshness/availability gate before referencing any tool or model.
- **`content-master`** - Added a **tool-demo pattern**: verify a tool actually does what the hook claims (read its real source, not the inspiration video), pre-build the demo + payoff artifact off-camera, and cadence-match a proven hook structure.

## [1.3.0] - 2026-06-06

### Added
- **`wipe-footprint`** - One-prompt digital footprint removal. Finds where your personal data (home address, phone, email, relatives) is exposed across data brokers and people-search sites, ranks everything by risk, and auto-writes every CCPA/GDPR opt-out and deletion request, filled in and ready to send, then saves a personal removal kit. Does for free what paid services like Incogni charge monthly for. Runs on Claude Code + built-in web search; Firecrawl (recon) and a Have I Been Pwned key (breach check) are optional enhancements. Ships with a 20+ broker opt-out registry, CCPA/GDPR/account-deletion templates, a per-skill README, and `config-templates/wipe-footprint-env.example`.

## [1.2.0] - 2026-05-04

### Added
- **`ig-analytics`** - Hourly Instagram analytics pipeline. Pulls per-post and account-level insights from the Meta Graph API into Supabase, mirrors live values into a Notion dashboard, and runs a daily Claude routine that classifies each post into Outlier / Average / Underperformer tiers with a 2-3 sentence "why" note. Includes Vercel cron handler, 5 utility scripts, init migration with RLS, and a parameterized Creative Director prompt template.
- **`video-editor`** - 9:16 short-form video pipeline using Hyperframes. Workflow wrapper that ships three style archetypes (sage-stack, editorial-magazine, screen-face-split) with deconstruction docs and pattern catalogs, the orange frosted-glass + karaoke pill overlay defaults, render contract gotchas, and a build-your-own-style-guide methodology.
- **Hyperframes suite (6 skills)** by Nate Herkai / Heygen, Apache 2.0 upstream: `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `gsap`, `website-to-hyperframes`, `claude-design-hyperframes`. Bundled so users can `git pull && cp -r skills/*` once and have the whole video stack. Attribution in `skills/THIRD_PARTY.md`.
- **`skills/THIRD_PARTY.md`** - Top-level attribution document covering all third-party skills (Hyperframes Suite, SEO Suite, Ads Suite, Blog Suite, last30days).

### Changed
- **`hooks`** - Major upgrade. Added 100-point 4-dimension ranking rubric (Scroll Stop / Word Economy / Pattern Interrupt / Authority Pack), tier gates (88+ Outlier, 78-87 Strong, 68-77 iterate, <68 reject), pre-flight checklist, triple-stacked hook rule (text + visual + verbal at second 0), Zeigarnik open-loop principle, outcome-over-audience framing, B/A vs open-loop framework choice, conversational glue rule, visual hook scoring layer, and dual CTA stack.
- **`content-scripting`** - Major upgrade. Cross-links to the new `hooks` rubric. Mandatory voice check pre-write step. Pre-flight + scored hook table required before script body. Refreshed voice and density rules. Dual CTA stack. References `carousel-builder`, `newsletter`, `blog-write`, `hand-raiser`.
- **`content-master`** - Minor cross-references to the new rubric.
- **README.md** - Bumped skill count to 69 (from 52). Added Instagram Analytics + Video Production categories to description.

### Repo
- The dual-repo experiment from the v1.0.0 release (`coopersimson96/ai-content-system-dev`) is being archived. This repo is the single source of truth.

## [1.0.0] - 2026-03-03

### Added
- Initial release with 52 skills across 7 categories
- Content Creation: content-master, content-scripting, content-pipeline, topic-researcher, hooks, inspiration-library, last30days
- Transcript & Lead Magnets: transcript, hand-raiser
- SEO: 13 skills (seo, seo-audit, seo-technical, seo-content, seo-schema, seo-sitemap, seo-page, seo-geo, seo-hreflang, seo-programmatic, seo-competitor-pages, seo-images, seo-plan)
- Ads: 13 skills (ads, ads-audit, ads-google, ads-meta, ads-linkedin, ads-tiktok, ads-microsoft, ads-youtube, ads-budget, ads-creative, ads-competitor, ads-landing, ads-plan)
- Blog: 13 skills (blog, blog-write, blog-rewrite, blog-analyze, blog-audit, blog-brief, blog-calendar, blog-chart, blog-geo, blog-outline, blog-repurpose, blog-schema, blog-seo-check, blog-strategy)
- Image Gen & Design: nano-banana, frontend-design
- E-commerce: ecommerce-cro, shopify-store-design
- Setup Skills: notion-setup, gdocs-setup
- Generic PDF generator (scripts/pdf_generator.py)
- Lead pages starter template (lead-pages-starter/)
- Config templates for Notion, Google Docs, and Supadata
- Shared scripts: gdocs_push.py, gdocs_formatter.py, gdrive_upload.py

