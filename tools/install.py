"""Installer voor de skillbibliotheek van Jelle, voor Claude Code en Codex.

Bedoeld om door een AI-assistent aangestuurd te worden (zie START-HIER.md), maar
ook met de hand bruikbaar. Schrijft nooit over een bestaande skill heen zonder
--vervang, en maakt in dat geval eerst een kopie.

    python tools/install.py lijst
    python tools/install.py plan      --doel claude --kies humanizer,content-master
    python tools/install.py installeer --doel claude --kies humanizer,content-master [--vervang] [--notitiemap PAD]
    python tools/install.py officieel --doel claude --familie ads [--vervang]
    python tools/install.py controleer --doel claude

--doel is claude, codex of beide. --kies aanvaardt skill-id's en familie-id's
(content, video, meta-instagram, overig), gescheiden door komma's.
Voeg --proef toe om te zien wat er zou gebeuren zonder iets te schrijven.
"""
import argparse
import json
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((PKG / "manifest.json").read_text(encoding="utf-8"))
HOME = Path.home()
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")
WINDOWS = platform.system() == "Windows"

SKILL_DIRS = {"claude": HOME / ".claude" / "skills", "codex": HOME / ".codex" / "skills"}
ACS = HOME / "ai-content-system"   # Coopers skills verwachten deze map voor scripts en output
COOPER = PKG / "vendor" / "cooper-ai-content-system"
NEEDS_SCRIPTS = {"content-scripting", "content-master", "hand-raiser", "gdocs-setup", "client-onboarding"}


# ---------------------------------------------------------------- manifest

def families():
    return {f["id"]: f for f in MANIFEST["families"]}


def skills():
    out = {}
    for f in MANIFEST["families"]:
        for s in f.get("skills", []):
            out[s["id"]] = {**s, "familie": f["id"]}
    return out


def resolve(choice):
    """Zet een keuzelijst om naar skills, met afhankelijkheden erbij."""
    fam, sk = families(), skills()
    wanted, notes, official = [], [], set()
    for item in [c.strip() for c in choice.split(",") if c.strip()]:
        if item in sk:
            wanted.append(item)
        elif item in fam and fam[item].get("per_skill"):
            wanted += [s["id"] for s in fam[item]["skills"] if not s.get("optioneel")]
        elif item in fam:
            official.add(item)
        else:
            sys.exit(f"Onbekend: {item}. Zie 'python tools/install.py lijst'.")
    i = 0
    while i < len(wanted):
        s = sk[wanted[i]]
        for dep in s.get("vereist", []):
            if dep not in wanted:
                wanted.append(dep)
                notes.append(f"{dep} komt mee, want {s['id']} heeft hem nodig")
        for famdep in s.get("vereist_familie", []):
            if famdep not in official:
                notes.append(f"{s['id']} werkt pas met de familie '{famdep}': installeer die met 'officieel --familie {famdep}'")
        i += 1
    return list(dict.fromkeys(wanted)), notes, official


def targets(doel):
    return ["claude", "codex"] if doel == "beide" else [doel]


# ---------------------------------------------------------------- kopiëren

def backup(path: Path, doel: str, label: str = ""):
    """Verplaats iets naar een kopiemap in plaats van het te verwijderen."""
    dest = SKILL_DIRS[doel].parent / f"skills-backup-{STAMP}" / (label or path.name)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(dest))
    return dest


CODEX_PATHS = [("~/.claude/skills", "~/.codex/skills"), ("$HOME/.claude/skills", "$HOME/.codex/skills"),
               ("~/.claude/content-system", "~/.codex/content-system")]


def rewrite_for_codex(folder: Path):
    """Skills verwijzen naar Claude-paden; in Codex staan ze elders."""
    for f in list(folder.rglob("*.md")) + list(folder.rglob("*.sh")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        new = t
        for old, repl in CODEX_PATHS:
            new = new.replace(old, repl)
        if new != t:
            f.write_text(new, encoding="utf-8")


def patch_product_demo_video(folder: Path):
    src = folder / "product-demo-video.md"
    if src.exists() and not (folder / "SKILL.md").exists():
        head = ("---\nname: product-demo-video\ndescription: Generate polished, animated product demo videos with "
                "Remotion, in portrait (1080x1920) and landscape (1920x1080), with background music and transition "
                "sounds. Triggers on \"demo video\", \"product video\", \"app demo\", \"showcase video\", "
                "\"promo video\", \"/demo-video\".\n---\n\n")
        (folder / "SKILL.md").write_text(head + src.read_text(encoding="utf-8"), encoding="utf-8")
        src.unlink()


def ensure_frontmatter(folder: Path, sid: str, uitleg: str):
    """Sommige skills missen de kop met naam en beschrijving; zonder die kop worden ze niet herkend."""
    f = next((x for x in (folder / "SKILL.md", folder / "skill.md") if x.exists()), None)
    if f and not f.read_text(encoding="utf-8").startswith("---"):
        desc = uitleg.replace('"', "'")
        head = f'---\nname: {sid}\ndescription: "{desc}"\n---\n\n'
        f.write_text(head + f.read_text(encoding="utf-8"), encoding="utf-8")


def clone_git_skill(spec: dict, dest: Path):
    """Skills die niet als kopie meegaan maar uit hun eigen repo komen, op een vaste versie."""
    subprocess.run(["git", "clone", "--quiet", spec["repo"], str(dest)], check=True)
    subprocess.run(["git", "-C", str(dest), "checkout", "--quiet", spec["ref"]], check=True)


def fill_notitiemap(folder: Path, notitiemap: str):
    f = folder / "SKILL.md"
    if notitiemap and f.exists():
        f.write_text(f.read_text(encoding="utf-8").replace("<<NOTITIEMAP>>", notitiemap), encoding="utf-8")


def setup_cooper_scripts(doel, vervang, proef, log):
    """Coopers gedeelde scripts op de plaatsen waar zijn skills ze zoeken."""
    places = [ACS / "scripts", SKILL_DIRS[doel] / "scripts"]
    for place in places:
        if place.exists() and not vervang:
            log.append(f"  bestaat al, ongemoeid gelaten: {place}")
            continue
        log.append(f"  scripts naar {place}")
        if proef:
            continue
        if place.exists():
            label = "scripts" if place.parent == SKILL_DIRS[doel] else "ai-content-system-scripts"
            log.append(f"  kopie van oude scripts naar {backup(place, doel, label)}")
        shutil.copytree(COOPER / "scripts", place, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(PKG / "patches" / "fonts", place / "fonts", dirs_exist_ok=True)
        gen = place / "pdf_generator.py"
        if gen.exists():  # lettertypes naast het script, zodat het ook op Windows werkt
            t = gen.read_text(encoding="utf-8")
            t = re.sub(r'_FONT_DIR = Path\.home\(\) / "Library" / "Fonts"',
                       '_FONT_DIR = Path(__file__).resolve().parent / "fonts"', t)
            gen.write_text(t, encoding="utf-8")
    if not proef:
        (ACS / "output").mkdir(parents=True, exist_ok=True)
        cfg = ACS / "config-templates"
        if not cfg.exists():
            shutil.copytree(COOPER / "config-templates", cfg)


def install(args):
    wanted, notes, official = resolve(args.kies)
    sk = skills()
    for doel in targets(args.doel):
        base = SKILL_DIRS[doel]
        log = [f"== {doel}: {base}"]
        if not args.proef:
            base.mkdir(parents=True, exist_ok=True)
        for sid in wanted:
            s = sk[sid]
            dest = base / sid
            if dest.exists() and not args.vervang:
                log.append(f"  OVERGESLAGEN {sid}: bestaat al (gebruik --vervang om te vervangen, met kopie)")
                continue
            if args.proef:
                log.append(f"  {'vervangt' if dest.exists() else 'installeert'} {sid}")
                continue
            old_copy = None
            if dest.exists():
                old_copy = backup(dest, doel)
                log.append(f"  kopie van oude {sid} naar {old_copy}")
            if "git" in s:
                clone_git_skill(s["git"], dest)
                log.append(f"  opgehaald uit {s['git']['repo']} ({s['git']['ref']})")
            else:
                shutil.copytree(PKG / s["bron"], dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "BRON.md"))
            if s.get("patch") == "product-demo-video-kop":
                patch_product_demo_video(dest)
            elif s.get("patch", "").startswith("kop-"):
                ensure_frontmatter(dest, sid, s["uitleg"])
            for keep in s.get("behoud", []):  # eigen instellingen en geschiedenis van de gebruiker terugzetten
                if old_copy and (old_copy / keep).exists():
                    target = dest / keep
                    if target.is_dir():
                        shutil.rmtree(target)
                    elif target.exists():
                        target.unlink()
                    (shutil.copytree if (old_copy / keep).is_dir() else shutil.copy2)(old_copy / keep, target)
                    log.append(f"  behouden: {sid}/{keep}")
            if sid == "wrap-up":
                fill_notitiemap(dest, args.notitiemap)
            if doel == "codex":
                rewrite_for_codex(dest)
            log.append(f"  geïnstalleerd: {sid}")
        if NEEDS_SCRIPTS & set(wanted):
            setup_cooper_scripts(doel, args.vervang, args.proef, log)
        print("\n".join(log))
    for n in notes:
        print(f"LET OP: {n}")
    for f in official:
        print(f"LET OP: familie '{f}' installeer je met: python tools/install.py officieel --doel {args.doel} --familie {f}")
    keys = sorted({k for sid in wanted for k in sk[sid].get("sleutels", [])})
    if keys:
        print("Nodig voor volledige werking (stel in bij eerste gebruik):")
        print("\n".join(f"  - {k}" for k in keys))


# ---------------------------------------------------------------- officiële installers

def run_official(args):
    fam = families()[args.familie]
    src = PKG / fam["bron"]
    main = {"ads": "ads", "seo": "seo", "blog": "blog"}[args.familie]
    for doel in targets(args.doel):
        base = SKILL_DIRS[doel]
        existing = [p for p in base.glob(f"{main}*") if p.is_dir() and (p.name == main or p.name.startswith(main + "-"))] if base.exists() else []
        if existing and not args.vervang:
            print(f"{doel}: er staan al {len(existing)} {main}-skills ({', '.join(p.name for p in existing[:5])}...). "
                  f"Niets gedaan. Gebruik --vervang om ze eerst naar een kopie te verplaatsen.")
            continue
        if args.proef:
            print(f"{doel}: zou {fam['naam']} installeren vanuit {src}" + (f" (en {len(existing)} bestaande eerst verplaatsen)" if existing else ""))
            continue
        for p in existing:
            backup(p, doel)
        if doel == "codex" and args.familie in ("seo", "blog"):
            # Geen officiële Codex-installer: de skills zelf kopiëren.
            for d in sorted((src / "skills").iterdir()):
                if d.is_dir():
                    shutil.copytree(d, base / d.name, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
                    rewrite_for_codex(base / d.name)
            print(f"codex: {args.familie}-skills gekopieerd naar {base}. De hulpagents zijn Claude-specifiek en niet meegenomen.")
            continue
        cmd = official_command(args.familie, doel, src)
        print(f"{doel}: {' '.join(cmd)}")
        res = subprocess.run(cmd, cwd=src)
        if res.returncode != 0 and args.familie == "seo":
            print("De SEO-installer kon GitHub niet bereiken of faalde. Terugval: kopie vanuit de momentopname.")
            for d in sorted((src / "skills").iterdir()):
                if d.is_dir():
                    shutil.copytree(d, base / d.name, dirs_exist_ok=True)
            agents = HOME / ".claude" / "agents"
            agents.mkdir(parents=True, exist_ok=True)
            for a in (src / "agents").glob("*.md"):
                shutil.copy2(a, agents / a.name)
        elif res.returncode != 0:
            sys.exit(f"Installer faalde met code {res.returncode}.")


def official_command(familie, doel, src):
    py_ok = sys.version_info[:2] in ((3, 11), (3, 12))
    if WINDOWS:
        ps = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(src / "install.ps1")]
        if familie == "ads":
            return ps + ["-Target", doel, "-Source", "local", "-RepoDir", str(src)] + ([] if py_ok else ["-NoDeps"])
        return ps
    sh = ["bash", str(src / "install.sh")]
    if familie == "ads":
        return sh + [f"--target={doel}", "--source=local", f"--repo-dir={src}"] + ([] if py_ok else ["--no-deps"])
    return sh


# ---------------------------------------------------------------- overzicht en controle

def lijst(_):
    for f in MANIFEST["families"]:
        mm = ""
        print(f"\n## {f['id']}: {f['naam']}{mm}\n   {f['uitleg']}")
        if not f.get("per_skill"):
            print(f"   Enkel als geheel: {f.get('reden_geen_per_skill', '')}")
            continue
        for s in f["skills"]:
            tag = " (aanbevolen)" if s.get("aanbevolen") else " (optioneel)" if s.get("optioneel") else ""
            print(f"   - {s['id']}{tag}: {s['uitleg']}")
    print("\n## plugins")
    for p in MANIFEST["plugins"]["lijst"]:
        print(f"   - {p['id']} ({p['marketplace']}): {p['uitleg']}")


def plan(args):
    args.proef = True
    install(args)


def controleer(args):
    sk = skills()
    for doel in targets(args.doel):
        base = SKILL_DIRS[doel]
        print(f"== {doel}: {base}")
        if not base.exists():
            print("  map bestaat niet")
            continue
        for d in sorted(p for p in base.iterdir() if p.is_dir()):
            f = next((x for x in (d / "SKILL.md", d / "skill.md") if x.exists()), None)
            if d.name in ("scripts",) or d.name.startswith("skills-backup"):
                continue
            if not f:
                print(f"  ZONDER SKILL.md: {d.name}")
                continue
            t = f.read_text(encoding="utf-8", errors="ignore")
            ok = t.startswith("---") and re.search(r"^name:", t, re.M) and re.search(r"^description:", t, re.M)
            if not ok:
                print(f"  kop onvolledig (naam/beschrijving): {d.name}")
            if "<<NOTITIEMAP>>" in t:
                print(f"  nog in te vullen: notitiemap in {d.name}")
        mine = [s for s in sk if (base / s).exists()]
        print(f"  {len(mine)} skills uit dit pakket aanwezig, {sum(1 for p in base.iterdir() if p.is_dir())} mappen in totaal")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("lijst").set_defaults(fn=lijst)
    for name, fn in (("plan", plan), ("installeer", install)):
        p = sub.add_parser(name)
        p.add_argument("--doel", choices=["claude", "codex", "beide"], required=True)
        p.add_argument("--kies", required=True)
        p.add_argument("--vervang", action="store_true")
        p.add_argument("--proef", action="store_true")
        p.add_argument("--notitiemap", default="")
        p.set_defaults(fn=fn)
    p = sub.add_parser("officieel")
    p.add_argument("--doel", choices=["claude", "codex", "beide"], required=True)
    p.add_argument("--familie", choices=["ads", "seo", "blog"], required=True)
    p.add_argument("--vervang", action="store_true")
    p.add_argument("--proef", action="store_true")
    p.set_defaults(fn=run_official)
    p = sub.add_parser("controleer")
    p.add_argument("--doel", choices=["claude", "codex", "beide"], required=True)
    p.set_defaults(fn=controleer)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
