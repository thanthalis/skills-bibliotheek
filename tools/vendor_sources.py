"""Haal vaste versies van de externe skillbronnen op naar vendor/ (skillbibliotheek).

Cooper-kopieen van ads/seo/blog/last30days worden weggelaten: die komen van hun eigen bron.

Gebruik (vanuit de repo-map):
    python tools/vendor_sources.py            # alle bronnen
    python tools/vendor_sources.py cooper     # één bron

Updaten naar een nieuwere versie: pas 'ref' hieronder aan, draai het script,
test de skills, en commit pas dan. Zo komt er nooit een ongeteste versie binnen.
"""
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VENDOR = REPO / "vendor"

# ref = tag of commit. 'drop' = paden in de bronrepo die niet mee hoeven (demo's, tests, CI).
SOURCES = {
    "cooper-ai-content-system": {
        "repo": "coopersimson96/ai-content-system", "ref": "ab7ec3f", "license": "Free to use, modify, and share (README)",
        "keep": ["skills", "scripts", "config-templates", "lead-pages-starter", "README.md", "CHANGELOG.md"],
        # Weg: vervangen skills en Coopers kopieen van bronnen die hun eigen map krijgen.
        "remove": ["skills/last30days/assets", "skills/last30days", "skills/carousel-gen", "skills/client-onboarding", "lead-pages-starter",
                   "skills/ads", "skills/seo", "skills/blog"] + [f"skills/{p}" for p in (
            "ads-audit ads-budget ads-competitor ads-creative ads-google ads-landing ads-linkedin ads-meta "
            "ads-microsoft ads-plan ads-tiktok ads-youtube blog-analyze blog-audit blog-brief blog-calendar "
            "blog-chart blog-geo blog-outline blog-repurpose blog-rewrite blog-schema blog-seo-check "
            "blog-strategy blog-write seo-audit seo-competitor-pages seo-content seo-geo seo-hreflang seo-images "
            "seo-page seo-plan seo-programmatic seo-schema seo-sitemap seo-technical").split()],
    },
    "claude-ads": {
        "repo": "AgriciDaniel/claude-ads", "ref": "v2.0.2", "license": "MIT",
        "drop": [".github", "tests", "evals"],
    },
    "claude-seo": {
        "repo": "AgriciDaniel/claude-seo", "ref": "v2.4.0", "license": "MIT",
        "drop": [".github", "tests", "screenshots", ".devcontainer"],
    },
    "claude-blog": {
        "repo": "AgriciDaniel/claude-blog", "ref": "v2.2.0", "license": "MIT",
        "drop": [".github", "tests", "reports"],
    },
    "humanizer": {
        "repo": "blader/humanizer", "ref": "v3.1.0", "license": "MIT",
        "drop": [".github"],
    },
    "last30days": {
        "repo": "mvanhorn/last30days-skill", "ref": "v3.25.0", "license": "MIT",
        "drop": [".github", "tests", "fixtures", "media", "assets", "docs"],
        "remove": ["skills/last30days/assets"],
    },
    "notebooklm": {
        "repo": "teng-lin/notebooklm-py", "ref": "v0.8.3", "license": "MIT",
        "keep": ["SKILL.md", "LICENSE", "README.md"],
    },
    "find-skills": {
        "repo": "vercel-labs/skills", "ref": "v1.7.0", "license": "MIT",
        "keep": ["skills/find-skills", "LICENSE", "README.md"],
    },
}
ALWAYS_DROP = {".git", "__pycache__", "node_modules", ".DS_Store"}


def run(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def fetch(name, spec):
    dst = VENDOR / name
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "src"
        run("git", "clone", "--quiet", "--filter=blob:none", f"https://github.com/{spec['repo']}.git", str(src))
        run("git", "checkout", "--quiet", spec["ref"], cwd=src)
        commit = run("git", "rev-parse", "HEAD", cwd=src)
        if dst.exists():
            shutil.rmtree(dst)
        dst.mkdir(parents=True)
        items = spec.get("keep") or [p.name for p in src.iterdir()]
        for item in items:
            p = src / item
            if not p.exists() or p.name in ALWAYS_DROP or item in spec.get("drop", []):
                continue
            target = dst / item
            if p.is_dir():
                shutil.copytree(p, target, ignore=shutil.ignore_patterns(*ALWAYS_DROP, "*.pyc"))
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, target)
        for rel in spec.get("remove", []):  # demobeelden en ander ballast binnen een bewaarde map
            if (dst / rel).exists():
                shutil.rmtree(dst / rel)
        for lic in ("LICENSE", "LICENSE.md", "LICENSE.txt", "NOTICE", "THIRD_PARTY_NOTICES.md"):
            if (src / lic).exists() and not (dst / lic).exists():
                shutil.copy2(src / lic, dst / lic)
    (dst / "BRON.md").write_text(
        f"# {name}\n\n"
        f"- Bron: https://github.com/{spec['repo']}\n"
        f"- Versie: {spec['ref']} (commit {commit})\n"
        f"- Opgehaald: {date.today().isoformat()}\n"
        f"- Licentie: {spec['license']}\n\n"
        f"Ongewijzigde momentopname. Eigen aanpassingen horen hier niet, maar in patches/.\n",
        encoding="utf-8",
    )
    size = sum(f.stat().st_size for f in dst.rglob("*") if f.is_file()) / 1048576
    print(f"{name}: {spec['ref']} ({commit[:7]}), {size:.1f} MB")


def main():
    wanted = sys.argv[1:] or list(SOURCES)
    for name in wanted:
        fetch(name, SOURCES[name])
    return 0


if __name__ == "__main__":
    sys.exit(main())
