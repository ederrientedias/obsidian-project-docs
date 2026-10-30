#!/usr/bin/env python3
"""Cobertura de arquivos por busca independente (Fase 4.1 da skill obsidian-project-docs).

Refaz as buscas mínimas da seção 3.2 sobre o PROJETO e lista, por categoria, os
arquivos com ocorrência que não aparecem em `fontes` de nenhuma nota do VAULT nem
em `_meta/Mapa Codigo-Notas.md`.

Somente leitura, sem rede, só biblioteca padrão. Não abre arquivos de segredo
(.env*, *.pem, *.key, credentials*, *serviceAccount*.json). Copie para /tmp antes de rodar.

O resultado são CANDIDATOS: cada arquivo não coberto precisa de triagem manual
(real → documentar; falso positivo → registrar o motivo no Relatório de Cobertura).

Uso:
  python3 -I cobertura_fontes.py <PROJETO> <VAULT> [--json]
         [--extra-pattern 'nome=regex' ...] [--exclude-dir nome ...]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

EXCLUDE_DIRS = {
    "node_modules", "dist", "build", ".angular", ".firebase", ".next", ".nx", "coverage", "tmp",
    ".git", ".svelte-kit", ".nuxt", ".output", ".turbo", ".cache", "vendor", "target", ".venv",
    "venv", "__pycache__", "Pods", ".gradle", ".dart_tool", ".idea", ".vscode",
}
TEXT_EXT = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".html", ".vue", ".svelte", ".astro", ".py", ".go",
    ".rb", ".java", ".kt", ".cs", ".php", ".dart", ".swift", ".rules", ".sql", ".yml", ".yaml",
}
EXTRA_FILES = {"firestore.indexes.json", "firebase.json", "ngsw-config.json", "package.json", "angular.json", "project.json"}
SKIP_FILE = re.compile(
    r"(^\.env(?!\.(example|sample)$))|\.pem$|\.key$|^credentials|serviceAccount.*\.json$|\.min\.js$|"
    r"\.generated\.|^database\.types\.ts$|(^|-)lock\.(json|yaml)$|^yarn\.lock$|^pnpm-lock\.yaml$",
    re.I,
)

PATTERNS: dict[str, str] = {
    "rotas": r"loadChildren|loadComponent|canActivate|canMatch|canDeactivate|redirectTo|\bpath:\s*['\"]|createBrowserRouter|<Route\b",
    "componentes": r"@Component\(|export default function [A-Z]|export function [A-Z]\w*\s*\(",
    "modais": r"\.open\(|bottomSheet|modalCtrl\.create|Dialog\b",
    "formularios": r"FormGroup|FormBuilder|formControlName|ngModel|\buseForm\(|<form\b",
    "dados": r"\bcollection\(|collectionGroup\(|\.doc\(|\bbatch\(|runTransaction\(|FieldValue\.|arrayUnion|arrayRemove|onSnapshot|valueChanges|snapshotChanges|\.from\(['\"]|\.rpc\(|uploadBytes|getDownloadURL|\bref\(",
    "http": r"http\.(get|post|put|patch|delete)\b|\bfetch\(|\baxios\b|httpResource|\bresource\(",
    "backend": r"\bonCall\b|\bonRequest\b|onDocument\w*|onSchedule|\bfunctions\.|app\.(get|post|put|patch|delete)\(|router\.(get|post|put|patch|delete)\(|@(Get|Post|Put|Patch|Delete)\(",
    "auth": r"signIn\w*|createUser\w*|signOut|sendPasswordReset\w*|customClaims|setCustomUserClaims|\broles?\b",
    "env": r"process\.env\.\w+|import\.meta\.env\.\w+|environment\.\w+|os\.environ|os\.getenv",
    "pendencias": r"\b(TODO|FIXME|HACK|XXX)\b",
    "links_externos": r"href=['\"]https?://",
    "testes": r"\b(describe|it|test)\(['\"]",
}


def iter_files(root: Path, extra_excludes: set[str]):
    excludes = EXCLUDE_DIRS | extra_excludes
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            entries = list(d.iterdir())
        except OSError:
            continue
        for e in entries:
            if e.is_dir():
                if e.name not in excludes and not e.is_symlink():
                    stack.append(e)
            elif e.is_file():
                if SKIP_FILE.search(e.name):
                    continue
                if e.suffix.lower() in TEXT_EXT or e.name in EXTRA_FILES:
                    yield e


def cited_paths(vault: Path) -> set[str]:
    """Paths cited in `fontes` of any note and anywhere in the Mapa Codigo-Notas."""
    cited: set[str] = set()
    path_like = re.compile(r"[\w.@~-]+(?:/[\w.@~\[\]()-]+)+\.\w+|[\w.-]+\.(?:ts|tsx|js|jsx|html|py|go|rules|sql|json|vue|svelte)\b")
    for p in vault.rglob("*.md"):
        if ".obsidian" in p.parts:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if "mapa codigo-notas" in p.stem.lower():  # aceita prefixo de projeto ("<Projeto> - Mapa Codigo-Notas")
            cited.update(path_like.findall(text))
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        front = text[3:end] if end != -1 else ""
        m = re.search(r"^fontes:\s*(.*)$", front, re.M)
        if not m:
            continue
        if m.group(1).strip().startswith("["):
            cited.update(x.strip().strip("'\"") for x in re.findall(r'"[^"]*"|[^,\[\]]+', m.group(1)) if x.strip())
        else:
            for line in front[m.end():].splitlines():
                item = re.match(r"^\s+-\s+(.*)$", line)
                if not item:
                    break
                cited.add(item.group(1).strip().strip("'\""))
    return {c.lstrip("./") for c in cited if c}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projeto", type=Path)
    ap.add_argument("vault", type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--extra-pattern", action="append", default=[], help="nome=regex (repetível)")
    ap.add_argument("--exclude-dir", action="append", default=[], help="pasta extra a ignorar (repetível)")
    args = ap.parse_args()

    proj, vault = args.projeto.expanduser().resolve(), args.vault.expanduser().resolve()
    patterns = dict(PATTERNS)
    for ep in args.extra_pattern:
        name, _, rx = ep.partition("=")
        if not rx:
            print(f"--extra-pattern inválido: {ep}", file=sys.stderr)
            return 2
        patterns[name] = rx
    compiled = {k: re.compile(v) for k, v in patterns.items()}

    cited = cited_paths(vault)
    hits: dict[str, dict[str, int]] = defaultdict(dict)  # categoria -> arquivo -> ocorrências
    for f in iter_files(proj, set(args.exclude_dir)):
        if vault == f or vault in f.parents:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = str(f.relative_to(proj))
        for cat, rx in compiled.items():
            n = len(rx.findall(text))
            if n:
                hits[cat][rel] = n

    def covered(rel: str) -> bool:
        # rel.lstrip("."): a extração de caminhos perde o ponto inicial de pastas como `.github/`
        return rel in cited or rel.lstrip(".") in cited or any(
            rel.endswith("/" + c) or c.endswith("/" + rel) for c in cited if "/" in c)

    report = {}
    for cat in patterns:
        files = hits.get(cat, {})
        unc = sorted(r for r in files if not covered(r))
        report[cat] = {
            "padrao": patterns[cat],
            "ocorrencias": sum(files.values()),
            "arquivos": len(files),
            "nao_cobertos": unc,
        }
    total_unc = len({f for r in report.values() for f in r["nao_cobertos"]})

    if args.json:
        print(json.dumps({"fontes_citadas": len(cited), "categorias": report, "arquivos_nao_cobertos": total_unc},
                         indent=2, ensure_ascii=False))
    else:
        print(f"Arquivos citados em fontes/Mapa: {len(cited)}")
        for cat, r in report.items():
            print(f"\n## {cat}: {r['ocorrencias']} ocorrências em {r['arquivos']} arquivos; não cobertos: {len(r['nao_cobertos'])}")
            print(f"   padrão: {r['padrao']}")
            for f in r["nao_cobertos"]:
                print(f"   - {f}")
        print(f"\nArquivos distintos não cobertos (candidatos para triagem): {total_unc}")
    return 1 if total_unc else 0


if __name__ == "__main__":
    sys.exit(main())
