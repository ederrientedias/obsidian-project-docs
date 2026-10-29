#!/usr/bin/env python3
"""Valida um VAULT gerado pela skill obsidian-project-docs (Fase 4.2).

Somente leitura, sem rede, só biblioteca padrão. Copie para /tmp antes de rodar.

Erros (exit 1):
  links quebrados, notas órfãs, YAML inválido (string sem aspas, tags com '#',
  tipo fora da lista, chave duplicada, ⚠️ sem status "parcial"), nomes de nota
  duplicados ou com caracteres proibidos, `[x]` sem link no Inventário, nota
  gerada sem `commit`/`fontes`, marcadores gerado desbalanceados, Mermaid com
  tipo não permitido ou atributo inválido no erDiagram, Home sem link para
  alguma seção, strings com cara de segredo.
Avisos:
  diagramas com mais de ~40 nós, rótulos Mermaid sem aspas, seções vazias,
  itens `[ ]` pendentes no Inventário.

Uso:
  python3 -I validate_vault.py <VAULT> [--vault-root <raiz>] [--home Home] [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

TIPOS = {"tela", "modal", "componente", "colecao", "api", "fluxo", "integracao", "servico", "meta"}
FORBIDDEN_NAME = re.compile(r'[/\\:*?"<>|#^\[\]]')
WIKILINK = re.compile(r"(!?)\[\[([^\]\[]+?)\]\]")
FENCE = re.compile(r"^\s*(```|~~~)\s*([\w-]*)")
INLINE_CODE = re.compile(r"`[^`\n]*`")
HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
MARK_START = "<!-- gerado:inicio -->"
MARK_END = "<!-- gerado:fim -->"
MERMAID_ALLOWED = ("flowchart", "sequencediagram", "erdiagram", "statediagram-v2")
MAX_NODES = 40
SECRET_PATTERNS = [
    ("chave privada", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("chave estilo Stripe/OpenAI", re.compile(r"\b(?:sk|pk|rk)[-_](?:live|test|proj)?[-_]?[A-Za-z0-9]{20,}\b")),
    ("token Slack", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("URL com credenciais", re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s/:@]+:[^\s/@]{3,}@")),
    ("URL assinada", re.compile(r"(?i)[?&](?:X-Amz-Signature|X-Goog-Signature|sig|token)=[A-Za-z0-9%._-]{16,}")),
    (
        "segredo atribuído",
        re.compile(
            r"(?i)\b[A-Z0-9_]*(?:SECRET|TOKEN|PASSWORD|PASSWD|API_?KEY|PRIVATE_?KEY)[A-Z0-9_]*\s*[=:]\s*"
            r"['\"]?(?!<|\$|\{|\*|x{3,}|your|example|exemplo|redacted|changeme|process\.|import\.|env\b)"
            r"[A-Za-z0-9/+_\-.]{16,}"
        ),
    ),
]


def norm(s: str) -> str:
    return unicodedata.normalize("NFC", s).strip().lower()


def split_frontmatter(text: str):
    """(frontmatter or None, body, body_line_offset)."""
    if not text.startswith("---"):
        return None, text, 0
    lines = text.splitlines()
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1 :]), i + 1
    return None, text, 0


SCALAR_OK = re.compile(r'^(?:".*"|\[.*\]|-?\d+(?:\.\d+)?|true|false|null|~|\|[-+]?|>[-+]?)$')


def check_yaml(front: str):
    """Minimal YAML checks without dependencies. Returns (props, problems)."""
    props: dict[str, object] = {}
    problems: list[str] = []
    current = None
    for n, raw in enumerate(front.splitlines(), 2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            problems.append(f"L{n}: indentação com tab")
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:(?:\s+(.*))?$", raw)
        if m:
            key, value = m.group(1), (m.group(2) or "").strip()
            if key in props:
                problems.append(f"L{n}: chave duplicada '{key}'")
            current = key
            if value == "":
                props[key] = []
                continue
            if value.count('"') % 2:
                problems.append(f"L{n}: aspas desbalanceadas em '{key}'")
            if not SCALAR_OK.match(value):
                problems.append(f"L{n}: valor string sem aspas duplas em '{key}': {value[:40]}")
            if value.startswith("["):
                inner = value[1:-1].strip()
                items = [v.strip() for v in re.findall(r'"[^"]*"|[^,]+', inner) if v.strip()]
                props[key] = [v.strip('"') for v in items]
            else:
                props[key] = value.strip('"')
            continue
        item = re.match(r"^\s+-\s+(.*)$", raw)
        if item and current is not None:
            v = item.group(1).strip()
            if not SCALAR_OK.match(v):
                problems.append(f"L{n}: item de '{current}' sem aspas duplas: {v[:40]}")
            if isinstance(props.get(current), list):
                props[current].append(v.strip('"'))
            continue
        if raw.startswith(" ") and current is not None:
            continue  # continuação de bloco
        problems.append(f"L{n}: linha YAML não reconhecida: {raw.strip()[:40]}")
    tags = props.get("tags")
    if isinstance(tags, list) and any(t.startswith("#") for t in tags):
        problems.append("tags com '#'")
    if isinstance(tags, str) and "#" in tags:
        problems.append("tags com '#'")
    return props, problems


def code_free_lines(body: str):
    """[(lineno, text)] outside fences, inline code blanked; plus mermaid blocks."""
    out, blocks, in_fence, lang, buf, start = [], [], False, "", [], 0
    for n, line in enumerate(body.splitlines(), 1):
        m = FENCE.match(line)
        if m:
            if not in_fence:
                in_fence, lang, buf, start = True, m.group(2).lower(), [], n
            else:
                if lang == "mermaid":
                    blocks.append((start, buf))
                in_fence = False
            continue
        if in_fence:
            buf.append(line)
        else:
            out.append((n, INLINE_CODE.sub("", line)))
    return out, blocks


NODE_DEF = re.compile(r"\b([A-Za-z_][\w-]*)\s*(\[\[|\[\(|\(\(|\[|\(|\{\{|\{|>)")
EDGE_IDS = re.compile(r"(?:^|[\s;&])([A-Za-z_][\w-]*)\s*(?=(?:-->|---|-\.->|==>|--[ox]|<-->|-\.-|--\s|\[|\(|\{|>|$))")


def check_mermaid(lines: list[str]):
    errors, warns = [], []
    body = [l for l in lines if l.strip() and not l.strip().startswith("%%")]
    if not body:
        return ["diagrama vazio"], warns
    head = body[0].strip().split()[0].lower()
    if head not in MERMAID_ALLOWED and head != "graph":
        errors.append(f"tipo Mermaid não permitido: {head}")
        return errors, warns
    if head == "graph":
        errors.append("use 'flowchart' em vez de 'graph'")
    nodes: set[str] = set()
    if head in ("flowchart", "graph"):
        for l in body[1:]:
            s = l.strip()
            if s.startswith(("subgraph", "end", "classDef", "class ", "style ", "linkStyle", "click ", "direction")):
                continue
            for m in NODE_DEF.finditer(s):
                nodes.add(m.group(1))
                after = s[m.end():].lstrip()
                if m.group(2) in ("[", "(", "{") and after and not after.startswith('"'):
                    warns.append(f"rótulo sem aspas no nó '{m.group(1)}'")
            for part in re.split(r"-->|---|-\.->|==>|<-->|-\.-|--[ox]|\|[^|]*\|", s):
                tok = part.strip().split("[")[0].split("(")[0].split("{")[0].split(">")[0].strip()
                if re.fullmatch(r"[A-Za-z_][\w-]*", tok or ""):
                    nodes.add(tok)
    elif head == "sequencediagram":
        for l in body[1:]:
            m = re.match(r"\s*(?:participant|actor)\s+([^\s]+)", l)
            if m:
                nodes.add(m.group(1))
            m = re.match(r"\s*([^\s:+-]+)\s*-[->x)]+[+-]?\s*([^\s:]+)\s*:", l)
            if m:
                nodes.update([m.group(1), m.group(2)])
    elif head == "erdiagram":
        in_entity = None
        for l in body[1:]:
            s = l.strip()
            m = re.match(r"^([A-Za-z_][\w-]*)\s*\{\s*$", s)
            if m:
                in_entity = m.group(1)
                nodes.add(in_entity)
                continue
            if s == "}":
                in_entity = None
                continue
            if in_entity:
                parts = s.split()
                if len(parts) >= 2 and not re.fullmatch(r"[A-Za-z0-9_]+", parts[1]):
                    errors.append(f"atributo inválido no erDiagram ({in_entity}): {parts[1]}")
                continue
            m = re.match(r"^([A-Za-z_][\w-]*)\s+\S+\s+([A-Za-z_][\w-]*)\s*:", s)
            if m:
                nodes.update([m.group(1), m.group(2)])
    elif head == "statediagram-v2":
        for l in body[1:]:
            for tok in re.findall(r"([A-Za-z_][\w]*|\[\*\])\s*(?:-->|$|:)", l):
                if tok != "[*]":
                    nodes.add(tok)
    if len(nodes) > MAX_NODES:
        warns.append(f"{head} com ~{len(nodes)} nós (máx ~{MAX_NODES}); divida por módulo")
    return errors, warns


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vault", type=Path, help="pasta do VAULT (contém Home.md)")
    ap.add_argument("--vault-root", type=Path, help="raiz do vault Obsidian, se VAULT for subpasta (unicidade de nomes)")
    ap.add_argument("--home", default="Home", help="nome da nota Home (padrão: Home)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    vault = args.vault.expanduser().resolve()
    if not vault.is_dir():
        print(f"Não é pasta: {vault}", file=sys.stderr)
        return 2
    root = (args.vault_root.expanduser().resolve() if args.vault_root else vault)

    def md_files(base: Path):
        return sorted(p for p in base.rglob("*.md") if not ({".obsidian", ".trash"} & set(p.parts)))

    doc_files = md_files(vault)
    all_files = md_files(root) if root != vault else doc_files

    by_name: dict[str, list[Path]] = defaultdict(list)
    for p in all_files:
        by_name[norm(p.stem)].append(p)
    attachments = {norm(p.name) for p in root.rglob("*") if p.is_file() and p.suffix.lower() != ".md" and ".obsidian" not in p.parts}
    rel_paths = {norm(str(p.relative_to(root).with_suffix(""))): p for p in all_files}

    keys = ("links_quebrados", "orfas", "yaml", "nomes", "inventario", "commit_fontes", "marcadores",
            "mermaid", "home", "segredos")
    wkeys = ("mermaid_avisos", "secoes_vazias", "pendentes")
    E = {k: [] for k in keys}
    W = {k: [] for k in wkeys}

    parsed = {}
    alias_index: dict[str, Path] = {}
    for p in all_files:
        text = p.read_text(encoding="utf-8", errors="replace")
        front, body, off = split_frontmatter(text)
        props, yprob = check_yaml(front) if front is not None else ({}, [])
        al = props.get("aliases")
        for a in (al if isinstance(al, list) else [al] if isinstance(al, str) and al else []):
            alias_index.setdefault(norm(a), p)
        parsed[p] = (text, front, body, off, props, yprob)

    def resolve(target: str):
        t = norm(target)
        if not t:
            return True
        if t.endswith(".md"):
            t = t[:-3]
        if t in rel_paths:
            return rel_paths[t]
        base = t.rsplit("/", 1)[-1]
        if base in by_name:
            return by_name[base][0]
        if t in alias_index:
            return alias_index[t]
        if base in attachments or t in attachments:
            return True
        return None

    inbound: dict[Path, int] = defaultdict(int)
    outlinks: dict[Path, set[Path]] = defaultdict(set)

    for p in doc_files:
        text, front, body, off, props, yprob = parsed[p]
        rel = str(p.relative_to(vault))
        generated = MARK_START in text or "tipo" in props or "commit" in props
        is_home = norm(p.stem) == norm(args.home) and p.parent == vault

        # Nome
        if FORBIDDEN_NAME.search(p.stem):
            E["nomes"].append(f"{rel}: caractere proibido no nome")
        if "_meta" in p.parts and p.stem != unicodedata.normalize("NFKD", p.stem).encode("ascii", "ignore").decode():
            E["nomes"].append(f"{rel}: nota de _meta com acento")

        # Marcadores
        s, e = text.count(MARK_START), text.count(MARK_END)
        seq = [m.group(0) for m in re.finditer(re.escape(MARK_START) + "|" + re.escape(MARK_END), text)]
        pos_ok = all(x == (MARK_START if i % 2 == 0 else MARK_END) for i, x in enumerate(seq))
        if s != e or not pos_ok:
            E["marcadores"].append(f"{rel}: {s} inicio × {e} fim")
        if generated and not is_home and s == 0:
            E["marcadores"].append(f"{rel}: nota gerada sem <!-- gerado:inicio -->")
        if is_home and s == 0:
            E["marcadores"].append(f"{rel}: Home sem bloco gerado")

        # YAML
        if generated and not is_home:
            if front is None:
                E["yaml"].append(f"{rel}: sem frontmatter")
            for pr in yprob:
                E["yaml"].append(f"{rel}: {pr}")
            tipo = props.get("tipo")
            if tipo not in TIPOS:
                E["yaml"].append(f"{rel}: tipo inválido ou ausente ({tipo!r})")
            for k in ("commit", "fontes"):
                if k not in props:
                    E["commit_fontes"].append(f"{rel}: sem '{k}'")
            if "⚠️" in body or "#nao-confirmado" in body:
                if props.get("status") != "parcial":
                    E["yaml"].append(f'{rel}: contém ⚠️ mas status não é "parcial"')
        elif is_home and front is not None:
            for pr in yprob:
                E["yaml"].append(f"{rel}: {pr}")

        # Links (frontmatter + corpo)
        lines, mermaids = code_free_lines(body)
        link_sources = [(off + n, l) for n, l in lines]
        if front:
            link_sources += [(i + 2, l) for i, l in enumerate(front.splitlines())]
        for n, line in link_sources:
            for _, raw in WIKILINK.findall(line):
                target = raw.split("|", 1)[0].split("#", 1)[0].split("^", 1)[0].strip()
                hit = resolve(target)
                if hit is None:
                    E["links_quebrados"].append(f"{rel}:L{n} [[{raw}]]")
                elif isinstance(hit, Path) and hit != p:
                    inbound[hit] += 1
                    outlinks[p].add(hit)

        # Mermaid
        for start, blk in mermaids:
            errs, warns = check_mermaid(blk)
            E["mermaid"] += [f"{rel}:L{off + start} {x}" for x in errs]
            W["mermaid_avisos"] += [f"{rel}:L{off + start} {x}" for x in sorted(set(warns))]

        # Seções vazias
        heads = [(i, HEADING.match(t)) for i, (_, t) in enumerate(lines)]
        heads = [(i, m) for i, m in heads if m]
        raw_body = body.splitlines()
        for idx, (i, m) in enumerate(heads):
            nxt = heads[idx + 1] if idx + 1 < len(heads) else None
            if nxt and len(nxt[1].group(1)) > len(m.group(1)):
                continue
            start_ln = lines[i][0]
            end_ln = lines[nxt[0]][0] - 1 if nxt else len(raw_body)
            chunk = [x for x in raw_body[start_ln:end_ln] if x.strip() and x.strip() not in (MARK_START, MARK_END)]
            if not chunk:
                W["secoes_vazias"].append(f"{rel}: ## {m.group(2)}")

        # Inventário
        if "_meta" in p.parts and norm(p.stem) == "inventario":
            for n, line in enumerate(body.splitlines(), 1):
                cm = re.match(r"^\s*[-*]\s+\[(.)\]\s", line)
                if not cm:
                    continue
                st = cm.group(1)
                if st.lower() == "x" and "[[" not in line:
                    E["inventario"].append(f"L{off + n}: [x] sem link: {line.strip()[:80]}")
                if st == " ":
                    W["pendentes"].append(f"L{off + n}: {line.strip()[:80]}")

        # Segredos
        for n, line in enumerate(text.splitlines(), 1):
            for label, pat in SECRET_PATTERNS:
                if pat.search(line):
                    E["segredos"].append(f"{rel}:L{n} {label}")
                    break

    # Nomes duplicados (vault inteiro)
    for name, paths in by_name.items():
        if len(paths) > 1 and any(vault == q or vault in q.parents for q in paths):
            E["nomes"].append("duplicado: " + " | ".join(str(q.relative_to(root)) for q in paths))

    # Órfãs
    home_path = next((p for p in doc_files if norm(p.stem) == norm(args.home) and p.parent == vault), None)
    if home_path is None:
        E["home"].append(f"{args.home}.md não encontrado na raiz do VAULT")
    for p in doc_files:
        if p == home_path or "_arquivo" in p.parts:
            continue
        if inbound[p] == 0:
            E["orfas"].append(str(p.relative_to(vault)))

    # Home linka todas as seções
    if home_path is not None:
        targets = outlinks[home_path]
        sections = [c for c in vault.iterdir()
                    if not c.name.startswith(".") and c.name != "_arquivo"
                    and (re.match(r"^\d\d ", c.name) or c.name in ("_meta",) or norm(c.stem) in ("glossário", "glossario"))]
        for c in sorted(sections):
            if c.is_file() and c.suffix == ".md":
                if c not in targets:
                    E["home"].append(f"Home não linka [[{c.stem}]]")
            elif c.is_dir():
                if not any(t == c or c in t.parents for t in targets):
                    E["home"].append(f"Home não linka nenhuma nota de '{c.name}/'")

    n_err = sum(len(v) for v in E.values())
    if args.json:
        print(json.dumps({"notas": len(doc_files), "erros": E, "avisos": W, "total_erros": n_err}, indent=2, ensure_ascii=False))
        return 1 if n_err else 0

    titles = {
        "links_quebrados": "Links quebrados", "orfas": "Notas órfãs", "yaml": "YAML inválido",
        "nomes": "Nomes duplicados/proibidos", "inventario": "Inventário: [x] sem link",
        "commit_fontes": "Notas sem commit/fontes", "marcadores": "Marcadores gerado",
        "mermaid": "Mermaid inválido", "home": "Home sem link para seção", "segredos": "Possíveis segredos",
        "mermaid_avisos": "Avisos Mermaid", "secoes_vazias": "Seções vazias", "pendentes": "Itens [ ] pendentes",
    }
    print(f"Notas verificadas: {len(doc_files)}")
    for group, label in ((E, "ERRO"), (W, "aviso")):
        for k, items in group.items():
            print(f"\n[{label}] {titles[k]}: {len(items)}")
            for it in items[:200]:
                print("  - " + it)
            if len(items) > 200:
                print(f"  ... +{len(items) - 200}")
    print("\nResultado: " + ("FALHOU" if n_err else "OK"))
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
