# Saved Brand Profiles

This directory holds saved brand profiles for `/ad-engine`. Each profile is one JSON file named `{brand-slug}.json`.

## How to use

- **First run for a brand:** `/ad-engine` (no args) walks discovery, then auto-saves the profile here.
- **Re-run for an existing brand:** `/ad-engine [brand-slug]` loads the profile and skips discovery.
- **List all brands:** `/ad-engine list`.
- **Edit a profile:** open the JSON directly or run `/ad-engine edit [brand-slug]`.
- **Delete a profile:** `/ad-engine delete [brand-slug]` (asks for confirmation).

## Profile schema

See `../templates/brand-profile.template.json` for the canonical schema. `example-brand.json` in this folder is a filled-in sample you can copy.

Fields populate progressively:
- **User-provided** (filled at first discovery): `brand`, `product_page_url`, `homepage_url`, `default_ad_account`, `default_objective`
- **Auto-extracted** (filled after first site scrape): `extracted_brand_palette`, `extracted_type_system`, `extracted_brand_voice_notes`
- **Run-tracked** (updated after every run): `last_run`, `run_count`, `canonical_photo_path`
- **Optional**: `notes` — free-text scratchpad for brand-specific quirks

## Privacy

Profiles can contain ad account IDs, brand voice notes, and product page URLs. Treat them as sensitive. Do not commit real profiles to a public repository, and never paste customer PII or access tokens into any field — tokens belong in environment variables or a local `.env`, never in a profile.
