"""Scan de repo op sleutels, tokens en sessies voor je commit.

Gebruik:  python tools/scan_secrets.py
Exitcode 0 = niets gevonden, 1 = verdachte regels (die worden getoond, zonder de waarde).
Vals alarm? Zet het pad in tools/scan_allowlist.txt, één per regel.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

PATTERNS = {
    "Anthropic/OpenAI-sleutel": r"sk-(ant-)?[A-Za-z0-9_-]{20,}",
    "GitHub-token": r"gh[pousr]_[A-Za-z0-9]{30,}",
    "Google API-sleutel": r"AIza[0-9A-Za-z_-]{30,}",
    "Notion-token": r"(ntn_|secret_)[A-Za-z0-9]{30,}",
    "GoHighLevel-token": r"pit-[a-f0-9]{8}-[a-f0-9-]{20,}",
    "Meta-token": r"EAA[A-Za-z0-9]{40,}",
    "Slack-token": r"xox[abpr]-[A-Za-z0-9-]{20,}",
    "Bearer-header": r"Bearer\s+[A-Za-z0-9._-]{20,}",
    "JWT": r"eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}",
    "Private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "Wachtwoord-toewijzing": r"(?i)(password|passwd|wachtwoord)\s*[:=]\s*['\"][^'\"\s]{6,}['\"]",
    "Sessie-cookie": r"\b(sessionid|csrftoken|ds_user_id)\b\"?\s*[:=]\s*\"?[A-Za-z0-9%:_-]{10,}",
}
SKIP_DIRS = {".git"}
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".ttf", ".otf", ".woff", ".woff2", ".mp4", ".zip"}


def main():
    allow = set()
    al = REPO / "tools/scan_allowlist.txt"
    if al.exists():
        allow = {l.strip() for l in al.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}
    hits = []
    for p in REPO.rglob("*"):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.parts) or p.suffix.lower() in SKIP_SUFFIXES:
            continue
        rel = p.relative_to(REPO).as_posix()
        if rel in allow or rel.startswith("tools/"):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for label, pat in PATTERNS.items():
                if re.search(pat, line):
                    hits.append(f"{rel}:{n}  {label}")
    # Mailadressen: enkel toegestaan in vendor/ (makers van open-source-pakketten, publiek
    # en nodig voor de naamsvermelding). Elders mag geen enkel echt adres staan.
    mail = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}")
    harmless = re.compile(r"@(example|voorbeeld|users\.noreply\.github|domain|yourdomain|email)\.", re.I)
    for p in REPO.rglob("*"):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.parts) or p.suffix.lower() in SKIP_SUFFIXES:
            continue
        rel = p.relative_to(REPO).as_posix()
        if rel.startswith(("vendor/", "tools/")) or rel in allow:
            continue
        for n, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for m in mail.finditer(line):
                if not harmless.search(m.group(0)):
                    hits.append(f"{rel}:{n}  Mailadres")
    if hits:
        print("VERDACHT, niet committen voor dit nagekeken is:")
        print("\n".join(sorted(set(hits))))
        return 1
    print("Geen sleutels of tokens gevonden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
