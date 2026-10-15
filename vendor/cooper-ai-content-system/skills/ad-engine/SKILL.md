---
name: ad-engine
description: |
  The 1-Prompt Meta Ads Engine. End-to-end Meta ad generation + paused
  campaign creation workflow. Asks 4 discovery questions, then runs the
  full pipeline: competitor intel (claude-ads /ads competitor), brand-site
  scraping for context, bulk image generation (kie.ai gpt-image-2), ad copy
  (claude-ads /ads creative), and paused Meta campaign creation (Meta Ads
  MCP). Dynamic Product Ad principles (brand compliance + variant matrix)
  are applied inline. Saves brand profiles for one-command re-runs.

  Trigger phrases (auto-fire on any of these in user prompt):
  - "/ad-engine" or "/ad engine"
  - "run the ad engine"
  - "launch ads for [brand]" / "build ads for [brand]" / "generate ads for [brand]"
  - "build a Meta campaign for [brand]" / "build the campaign for [brand]"
  - "20 ads for [brand]" / "20 Meta ads for [brand]"
  - "automate Meta ads" / "automate my Meta ads"
  - "one prompt ads" / "one-prompt ads"
  - "fresh ad batch" / "generate a fresh ad batch"
context: conversation
---

# Ad Engine — The 1-Prompt Meta Ads Engine

One slash command + 4 questions = 20 brand-compliant Meta ads + a paused campaign in your Ads Manager. ~90 seconds of execution, ~$1.20 in image credits. Campaigns are always created PAUSED for review — the skill never auto-launches spend.

---

## Required Tools (Pre-Flight Check)

Before running, the skill verifies these are connected. If any are missing it tells the user to set them up first.

| Tool | Why it's needed | Setup |
|---|---|---|
| **claude-ads skill** | `/ads competitor` (intel) + `/ads creative` (copy) | `/plugin install claude-ads@agricidaniel-claude-ads` |
| **Meta Ads MCP** | Campaign + ad set + ad creation | Connect at `https://mcp.facebook.com/ads` via Claude Settings → Connectors |
| **kie-image MCP** | Bulk image-to-image generation | Install kie-image MCP, add API key |
| **Firecrawl** (optional) | Brand site scraping for richer context | `firecrawl --status` should return Authenticated |

**Pre-flight implementation:** at the start of every run, the skill checks:
- `/plugin list` includes `claude-ads@agricidaniel-claude-ads`
- Settings → Connectors lists `mcp.facebook.com/ads` as Connected
- kie-image MCP responds to a simple test call
- `firecrawl --status` returns Authenticated

If any fail → halt with a clear error + setup link.

---

## Process — The 5-Stage Run

### Stage 0: Consult your hook bank (before creative)

Before writing any ad copy, optionally pull proven hook patterns for the brand's category. If you use the `hooks` skill or an Inspiration Library, surface 5-10 high-performing hooks in the brand's topic at ≤14 words and use them as structural patterns for the headline + primary text. Never copy verbatim — use as patterns. If you have no hook bank, skip this stage and let `/ads creative` generate from scratch.

### Stage A: Discovery (4 questions, ~30 sec)

Ask all 4 upfront so the user can answer in one paste. If a saved brand profile exists for the named brand, skip to Stage B.

**Q1 — Brand name + product page URL:**
> "What's the brand name + product page URL? Format: `Brand: [name]. URL: [product-page-url]`"

**Q2 — Canonical product photo:**
> "Drop in 1 high-res canonical product photo (≥2000px, single isolated product, color-accurate). The workflow will scrape additional angles, model shots, and lifestyle photos from the product page automatically — you don't need to upload more than one."

**Q3 — Campaign objective + ad account:**
> "What's the campaign objective and which Meta ad account? Format: `Objective: [Sales/Conversions/Traffic]. Ad account: [account name or ID]`. Default Sales if not specified."

**Q4 — Variant count + angle override (optional):**
> "Variant count? Default is 20 (5 angles × 4 format variants). Reply 'default' or specify e.g. '12 (4 angles × 3 variants)'. Optional: any specific angles you want to lock in (otherwise /ads competitor will choose the top 5 winners)."

### Stage B: Confirm (10 sec)

Echo back the brief in summary form:

```
🎯 Brief locked:
   Brand: [X]
   Product page: [URL]
   Photo: [filename] (loaded)
   Objective: [Y]
   Ad account: [Z]
   Variants: [N] ([angles] × [formats])
   Estimated time: ~90 sec
   Estimated cost: $[N × 0.06]

Type 'go' to run, or describe a change.
```

Wait for `go` or a change request before proceeding.

### Stage C: Execute (~90 sec)

Run the 4-stage workflow by sending this single prompt to Claude (discovery variables filled in):

```
Brand: {brand_name}.
Product page URL: {product_page_url}.
Canonical product photo: attached as {photo_filename}.

Step 1: Run /ads competitor to scrape my brand site (for palette,
type, voice, and additional product images) AND the Meta Ad Library
to surface the top {n_angles} angles competitors are winning with
right now.

Step 2: Use kie.ai gpt-image-2 (image-to-image) to generate
{n_variants} static ads, {n_angles} angles times {n_formats} format
variants each (lifestyle, studio, testimonial-style, before-after).
Use the canonical photo as primary seed and the scraped page images
as secondary seeds. Apply the extracted brand palette and type
system. Apply Dynamic Product Ad principles: same product,
brand-compliant, varied by angle.

Step 3: Run /ads creative to write a 40-character headline and
125-character primary text paired to each static. Match the brand
voice extracted from the site.

Step 4: Create a paused Meta campaign via the Meta Ads MCP in
account {ad_account} with objective {objective}. {n_angles} ad sets
grouped by angle, all {n_variants} ads added, ready for review.
```

**Dynamic Product Ad principles (applied inline in Step 2):** keep the same product across every variant, stay brand-compliant (extracted palette + type + voice), and vary only by angle and format. Structure the output as a variant matrix — `{n_angles}` angles × `{n_formats}` formats — so each ad set maps to one angle and holds its format variants. This keeps the batch coherent and lets you read winners by angle once the campaign runs.

The skill streams progress updates as each step runs:
- `🔍 Stage 1: Researching competitors + scraping brand site...` (~30 sec)
- `🎨 Stage 2: Generating {n} variants...` (~30 sec, progress bar 1/N → N/N)
- `✍️  Stage 3: Writing headlines + primary text...` (~10 sec)
- `📤 Stage 4: Building paused campaign in Ads Manager...` (~20 sec)

### Stage D: Review (instant)

Returns a summary block:

```
✅ Campaign built and paused in Ads Manager

   Campaign ID: [id]
   Open in Ads Manager: [url]
   Total time: [Xs]
   Total cost: $[Y]

   📊 5 ad sets created:
      • [Angle 1 name] — 4 ads
      • [Angle 2 name] — 4 ads
      • [Angle 3 name] — 4 ads
      • [Angle 4 name] — 4 ads
      • [Angle 5 name] — 4 ads

   Status: PAUSED — review and unpause when ready.
```

### Stage E: Save Profile (auto)

Save the brand profile to `~/.claude/skills/ad-engine/brands/{brand-slug}.json` so future runs can skip Stage A. See `templates/brand-profile.template.json` for the schema:

```json
{
  "brand": "Example Brand",
  "product_page_url": "https://yoursite.com/products/example",
  "homepage_url": "https://yoursite.com",
  "default_ad_account": "act_XXXXXXXXX",
  "default_objective": "Sales",
  "default_variants": 20,
  "default_angles": 5,
  "default_formats": ["lifestyle", "studio", "testimonial-style", "before-after"],
  "extracted_brand_palette": ["#7C3AED", "#F5F3ED", "#171717"],
  "extracted_type_system": "Inter / GT America",
  "extracted_brand_voice_notes": "Punchy, contemporary, slightly irreverent",
  "last_run": "2026-01-01T00:00:00Z",
  "run_count": 1
}
```

---

## Sub-Commands / Natural Language Patterns

The skill responds to these patterns:

| Invocation | Behavior |
|---|---|
| `/ad-engine` (no args) | Fresh run with full Stage A discovery |
| `/ad-engine [brand]` | Look up saved profile for `[brand]`. If found, skip to Stage B with all defaults. If not found, fall back to fresh discovery. |
| `/ad-engine new [brand]` | Force fresh discovery even if saved profile exists |
| `/ad-engine list` | List all saved brand profiles + their last-run dates |
| `/ad-engine show [brand]` | Print the saved profile JSON for review |
| `/ad-engine edit [brand]` | Open the saved profile for inline editing |
| `/ad-engine delete [brand]` | Remove a saved profile after confirmation |
| `/ad-engine run [brand] variants 40` | Use saved profile but override variant count |
| `/ad-engine run [brand] angles 3` | Use saved profile but override angle count |
| `"build me 20 Meta ads for [brand]"` | Same as `/ad-engine [brand]` (natural-language path) |
| `"run the ad engine for [brand]"` | Same as above |
| `"fresh ad batch for [brand]"` | Same as above (weekly-cadence framing) |

---

## Tool Coordination Map

When the workflow runs, the skill orchestrates these tools:

| Stage | Tool | Visible to user? |
|---|---|---|
| A. Discovery | (skill itself, prompts user) | Yes |
| B. Confirm | (skill itself, summary block) | Yes |
| C-1. Competitor + site scrape | `/ads competitor` (claude-ads) + Firecrawl in the background | Partially — agent output streams but raw firecrawl scraping is silent |
| C-2. Image generation | `mcp__kie-image__edit_image` (image-to-image) | Yes — progress bar streams |
| C-3. Copy | `/ads creative` (claude-ads) | Yes — copy lines stream as written |
| C-4. Campaign build | Meta Ads MCP (`mcp.facebook.com/ads`) | Yes — every write requires user approval through chat |

---

## What The User Sends vs What The Workflow Pulls

This is the value prop the skill makes explicit during Stage A:

| Source | What lands in the workflow |
|---|---|
| User uploads | 1 canonical product photo |
| User pastes | Brand name + product page URL + (optional) homepage URL |
| User specifies | Campaign objective + ad account + variant count |
| `/ads competitor` pulls | Top winning angles + hook patterns + format mix from Meta Ad Library |
| Firecrawl pulls (silent) | Additional product images, model shots, lifestyle photos, brand palette, type, voice |
| DPA principles (built in) | Variant matrix structure, brand-compliance gates, angle-per-ad-set mapping |
| kie.ai generates | 20 brand-compliant static ad creatives |
| `/ads creative` writes | 20 paired headlines + primary text |
| Meta MCP builds | The paused campaign with N ad sets |

---

## Failure Modes & Recovery

| Failure | What the skill does |
|---|---|
| Pre-flight tool missing | Halt + clear setup instructions for the missing tool |
| Firecrawl scrape fails (e.g. JS-heavy SPA) | Continue without site context — fall back to "user-uploaded photo only" mode + log warning |
| kie.ai rate-limited or down | Halt at Stage C-2, save partial state, suggest retry |
| `/ads competitor` returns no data | Halt + ask user to manually specify 5 angles |
| Meta MCP write fails | Halt at Stage C-4, keep generated assets, suggest retry or manual upload |
| User says "abort" at Stage B | Discard discovery, no API calls fired |

State checkpointing: writes intermediate output to `~/.claude/skills/ad-engine/runs/{run-id}/` so a partial run can be resumed.

---

## Defaults (Edit Inline When Needed)

| Default | Value | Override |
|---|---|---|
| Variants | 20 | `variants N` |
| Angles | 5 | `angles N` |
| Formats per angle | 4 (lifestyle, studio, testimonial, before-after) | `formats [list]` |
| Objective | Sales | `objective [name]` |
| Image model | kie.ai gpt-image-2 | not configurable in v1 |
| Image-to-image seed | canonical photo + scraped page images | not configurable in v1 |
| Campaign status | PAUSED (always — never auto-launches) | not configurable for safety |

---

## Output Files

After every successful run:

```
~/.claude/skills/ad-engine/runs/{run-id}/
├── brief.json              # Stage B confirmed brief
├── competitor-intel.json   # Stage C-1 output
├── statics/                # Stage C-2 generated images
│   ├── angle1-lifestyle.png
│   ├── angle1-studio.png
│   ├── angle1-testimonial.png
│   ├── angle1-before-after.png
│   ├── angle2-lifestyle.png
│   └── ... (20 total)
├── copy.json               # Stage C-3 headlines + primary text
└── campaign.json           # Stage C-4 final campaign URLs + IDs
```

This makes the run reproducible, auditable, and replayable.

---

## Cross-Skill References

- **`/ads competitor`** — primary intel tool, runs in Stage C-1.
- **`/ads creative`** — primary copy tool, runs in Stage C-3.
- **`/ads meta`** — NOT used here (that's an audit skill for existing accounts). This skill creates new campaigns, doesn't audit them.

---

## When NOT To Use This Skill

- B2B service ads (no product catalog)
- Brand-launch / awareness campaigns (no SKU)
- Single hero-product launches where you want one perfect ad, not 20 variants
- Video-first campaigns
- Catalogs under 5 SKUs (overkill; one good static + manual upload is faster)

For these, fall back to manual `/ads plan [type]` or one-off creative work.

---

## Versioning

- v1.0: Initial release. 4-stage pipeline, brand-profile saving, natural-language invocation.
- v1.1 (planned): Scheduled mode (`/ad-engine schedule weekly`) that wraps the workflow in a cron job.
- v1.2 (planned): Multi-platform reformat (`/ad-engine reformat tiktok`) that takes a winning batch and translates per-platform mood.
- v1.3 (planned): Per-Product Video mode (`/ad-engine video`).
