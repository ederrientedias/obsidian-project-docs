#!/usr/bin/env python3
"""Validate an Obsidian documentation folder produced by obsidian-project-docs.

Checks: broken wikilinks, orphan notes, missing frontmatter / required
properties, note-name collisions inside the vault, empty sections and strings
that look like secrets. Standard library only.

Usage:
    python validate_vault.py <docs_folder> [--vault-root <vault>] [--json]

Exit code is 1 when errors (broken links, secrets, collisions) are found.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REQUIRED_PROPS = ("type", "project", "status", "last_reviewed")
WIKILINK = re.compile(r"(!?)\[\[([^\]\[]+?)\]\]")
FENCE = re.compile(r"^(```|~~~)")
INLINE_CODE = re.compile(r"`[^`\n]*`")
HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
SECRET_PATTERNS = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("Stripe/OpenAI-style key", re.compile(r"\b(?:sk|pk|rk)[-_](?:live|test|proj)?[-_]?[A-Za-z0-9]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("URL with credentials", re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s/:@]+:[^\s/@]{3,}@")),
    (
        "assigned secret",
        re.compile(
            r"(?i)\b[A-Z0-9_]*(?:SECRET|TOKEN|PASSWORD|PASSWD|API_?KEY|PRIVATE_?KEY)[A-Z0-9_]*\s*[=:]\s*"
            r"['\"]?(?!<|\$|\{|\*|x{3,}|your|example|redacted|changeme|process\.|import\.|env\b)"
            r"[A-Za-z0-9/+_\-.]{16,}"
        ),
    ),
]


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines()
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1 :])
    return None, text


def parse_props(front: str) -> tuple[set[str], list[str]]:
    """Return (top-level keys, aliases). Minimal YAML reading, no dependency."""
    keys: set[str] = set()
    aliases: list[str] = []
    current = None
    for raw in front.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", raw)
        if m:
            current = m.group(1)
            keys.add(current)
            value = m.group(2).strip()
            if current == "aliases" and value:
                value = value.strip("[]")
                aliases += [v.strip().strip("'\"") for v in value.split(",") if v.strip()]
            continue
        item = re.match(r"^\s+-\s+(.*)$", raw)
        if item and current == "aliases":
            aliases.append(item.group(1).strip().strip("'\""))
    return keys, aliases


def strip_code(body: str) -> list[tuple[int, str]]:
    """Body lines outside fenced code, with inline code blanked. (lineno, text)."""
    out, in_fence = [], False
    for n, line in enumerate(body.splitlines(), 1):
        if FENCE.match(line.strip()):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append((n, INLINE_CODE.sub("", line)))
    return out


def link_target(raw: str) -> str:
    target = raw.split("|", 1)[0].split("#", 1)[0].split("^", 1)[0].strip()
    return target


def norm(name: str) -> str:
    return name.strip().lower()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docs", type=Path, help="documentation folder inside the vault")
    ap.add_argument("--vault-root", type=Path, help="vault root, to resolve links and detect name collisions vault-wide")
    ap.add_argument("--home", help="name of the home note (exempt from the orphan check)")
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    args = ap.parse_args()

    docs = args.docs.resolve()
    if not docs.is_dir():
        print(f"Not a folder: {docs}", file=sys.stderr)
        return 2
    root = (args.vault_root or docs).resolve()

    def md_files(base: Path):
        return [p for p in base.rglob("*.md") if ".obsidian" not in p.parts and ".trash" not in p.parts]

    doc_files = md_files(docs)
    all_files = md_files(root) if root != docs else doc_files

    by_name: dict[str, list[Path]] = defaultdict(list)
    for p in all_files:
        by_name[norm(p.stem)].append(p)
    # Non-markdown attachments are valid link targets too.
    attachments = {norm(p.name) for p in root.rglob("*") if p.is_file() and p.suffix.lower() != ".md"}
    rel_paths = {norm(str(p.relative_to(root).with_suffix("")).replace("\\", "/")) for p in all_files}

    alias_index: dict[str, Path] = {}
    report = {k: [] for k in ("broken_links", "orphans", "frontmatter", "collisions", "empty_sections", "secrets")}
    inbound: dict[Path, int] = defaultdict(int)
    parsed = {}

    for p in all_files:
        text = p.read_text(encoding="utf-8", errors="replace")
        front, body = split_frontmatter(text)
        keys, aliases = parse_props(front) if front is not None else (set(), [])
        for a in aliases:
            alias_index.setdefault(norm(a), p)
        parsed[p] = (front, body, keys, text)

    def resolve(target: str) -> Path | None | bool:
        t = norm(target)
        if not t:
            return True  # same-note heading link
        if t.endswith(".md"):
            t = t[:-3]
        if t in rel_paths:
            base = t.rsplit("/", 1)[-1]
            return by_name[base][0] if by_name.get(base) else True
        base = t.rsplit("/", 1)[-1]
        if base in by_name:
            return by_name[base][0]
        if t in alias_index:
            return alias_index[t]
        if base in attachments or t in attachments:
            return True
        return None

    for p in doc_files:
        front, body, keys, text = parsed[p]
        rel = str(p.relative_to(docs))
        if front is None:
            report["frontmatter"].append({"note": rel, "problem": "no frontmatter"})
        else:
            missing = [k for k in REQUIRED_PROPS if k not in keys]
            if missing:
                report["frontmatter"].append({"note": rel, "problem": "missing: " + ", ".join(missing)})

        lines = strip_code(body)
        for n, line in lines:
            for _, raw in WIKILINK.findall(line):
                target = link_target(raw)
                hit = resolve(target)
                if hit is None:
                    report["broken_links"].append({"note": rel, "line": n, "link": raw})
                elif isinstance(hit, Path) and hit != p:
                    inbound[hit] += 1

        # Empty sections: a heading followed directly by a same-or-higher heading or EOF.
        heads = [(i, HEADING.match(t)) for i, (_, t) in enumerate(lines)]
        heads = [(i, m) for i, m in heads if m]
        for idx, (i, m) in enumerate(heads):
            end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
            content = [t for _, t in lines[i + 1 : end] if t.strip()]
            next_level = len(heads[idx + 1][1].group(1)) if idx + 1 < len(heads) else 0
            # Count fenced blocks between headings as content (they were stripped).
            if not content and (next_level == 0 or next_level <= len(m.group(1))):
                raw_body = body.splitlines()
                start_ln = lines[i][0]
                end_ln = lines[end][0] - 1 if end < len(lines) else len(raw_body)
                if not any(s.strip() for s in raw_body[start_ln:end_ln]):
                    report["empty_sections"].append({"note": rel, "heading": m.group(2)})

        for n, line in enumerate(text.splitlines(), 1):
            for label, pat in SECRET_PATTERNS:
                if pat.search(line):
                    report["secrets"].append({"note": rel, "line": n, "kind": label})
                    break

    for name, paths in by_name.items():
        if len(paths) > 1 and any(docs in p.parents or p.parent == docs for p in paths):
            report["collisions"].append({"name": paths[0].stem, "paths": [str(p.relative_to(root)) for p in paths]})

    home = norm(args.home) if args.home else None
    for p in doc_files:
        is_home = norm(p.stem) == home if home else (p.parent == docs and p.stem.lower().endswith("home"))
        if not is_home and inbound[p] == 0 and "_meta" not in p.parts:
            report["orphans"].append(str(p.relative_to(docs)))

    errors = len(report["broken_links"]) + len(report["secrets"]) + len(report["collisions"])
    if args.json:
        print(json.dumps({"notes": len(doc_files), **report}, indent=2, ensure_ascii=False))
        return 1 if errors else 0

    print(f"Notes checked: {len(doc_files)}")
    sections = [
        ("Broken wikilinks", "broken_links", lambda r: f"{r['note']}:{r['line']}  [[{r['link']}]]"),
        ("Possible secrets", "secrets", lambda r: f"{r['note']}:{r['line']}  {r['kind']}"),
        ("Note-name collisions", "collisions", lambda r: f"{r['name']}: " + " | ".join(r["paths"])),
        ("Orphan notes (no inbound links)", "orphans", lambda r: r),
        ("Frontmatter problems", "frontmatter", lambda r: f"{r['note']}  {r['problem']}"),
        ("Empty sections", "empty_sections", lambda r: f"{r['note']}  ## {r['heading']}"),
    ]
    for title, key, fmt in sections:
        items = report[key]
        print(f"\n{title}: {len(items)}")
        for r in items:
            print("  - " + fmt(r))
    print("\nResult: " + ("FAIL" if errors else "OK (review warnings above)" if any(report.values()) else "OK"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
