# obsidian-project-docs

An agent skill that investigates a software project end to end and writes a structured, interlinked, evidence-backed knowledge base into an Obsidian vault.

The result is meant to let a developer or an AI agent who has never seen the project understand its architecture and work on it without reading the whole codebase first.

## What it does

Every run is a **full X-ray** of the project: there is no quick or survey mode. The skill reads the whole codebase and goes through five phases:

0. **Recon and scope**: validates the vault (must contain `Home.md`), reads it, finds every app/package, stack and versions.
1. **Mechanical inventory** (`_meta/Inventario.md`): routes, screens, modals, components, forms, DB and HTTP calls, collections/tables, functions/endpoints, services/stores, integrations, env vars, tests, TODOs, each with `file → symbol` and the exact destination note name. Stops for confirmation when the inventory is large (>~150 items) or has several apps.
2. **Documentation in batches** (optionally with subagents): one note per screen, modal, shared component, collection, API, service, integration and flow, tracing every action down to the concrete read, write or navigation.
3. **Cross-cutting view**: navigation map, architecture, ER diagrams, permission and data matrices, entity state machines, user messages, cascades, storage, environments, PWA/SSR, plus mandatory cross-checks (query × index, write × security rule).
4. **Audit**: independent re-search mapped to each note's `fontes` (`cobertura_fontes.py`), vault validation (`validate_vault.py`), independent verification of the heaviest notes, and a coverage report.

Re-running on a documented vault switches to **update mode**: diff since the recorded commit, full re-inventory, reprocess only notes whose sources changed, archive notes of removed code, full audit again.

The generated vault is written in Portuguese (pt-BR).

## Principles

- **Read-only, no side effects**: no installs, builds, app/test runs, cloud CLIs, network or real database access. Runtime behavior is inferred from code and labeled as such.
- **Evidence with confidence levels**: `file → symbol (Lx)` citations, line numbers from tools; `Inferido` and `⚠️ Não confirmado` labels.
- **No secrets or personal data**: key names only, synthetic examples only; committed config is flagged as a risk.
- **Human content preserved**: generated content lives between `<!-- gerado:inicio -->` / `<!-- gerado:fim -->`.
- **Plain Obsidian**: wikilinks, properties, callouts and Mermaid (flowchart, sequence, ER, state). No community plugins.
- **Honest partial over shallow complete**: when context runs out it stops at a batch boundary and reports `PARCIAL`.

## Install

### Claude Code plugin (recommended)

Inside Claude Code:

```text
/plugin marketplace add ederrientedias/obsidian-project-docs
/plugin install obsidian-project-docs@obsidian-project-docs
```

Update later with `/plugin marketplace update obsidian-project-docs`.

### Claude Code, as a plain skill

```bash
git clone https://github.com/ederrientedias/obsidian-project-docs /tmp/opd
cp -r /tmp/opd/skills/obsidian-project-docs ~/.claude/skills/
```

Use `.claude/skills/` inside a repository instead of `~/.claude/skills/` to install it for one project only.

### Claude apps

Zip the `skills/obsidian-project-docs` folder and upload it in the skills settings.

## Use

Open the agent in the project you want documented and ask, for example:

```text
/obsidian-project-docs ~/Vaults/Acme
```

```text
Documenta esse projeto no Obsidian, vault em ~/Vaults/Acme.
```

```text
O código mudou bastante desde o mês passado. Atualiza a documentação no vault ~/Vaults/Acme.
```

The vault folder must already exist and contain a `Home.md`; if it is missing the skill stops and asks. It writes through the Obsidian MCP only when it can confirm the MCP points to the same vault, otherwise straight to the files.

## Layout

```text
.claude-plugin/
  plugin.json                         plugin manifest
  marketplace.json                    lets the repo be added as a marketplace
skills/obsidian-project-docs/
  SKILL.md                            workflow and core rules
  references/
    fase-0-1-inventario.md            recon, scope, mandatory searches, inventory, gate
    fase-2-documentacao.md            batches, subagents, trace-to-effect, per-area coverage
    templates.md                      templates per note type, inventory and reports
    formato-obsidian.md               names, frontmatter, markers, citations, Mermaid
    fase-3-transversal.md             cross-cutting notes and mandatory cross-checks
    fase-4-auditoria.md               audit steps and completion criteria
    ferramentas-externas.md           curated third-party tools (ideas only, never run)
  scripts/
    validate_vault.py                 links, orphans, YAML, names, inventory, markers, Mermaid, secrets
    cobertura_fontes.py               re-runs the searches and lists files no note cites
evals/
  evals.json                          test prompts for iterating on the skill
```

## Validate a generated vault

Both scripts are read-only, network-free and standard-library only.

```bash
python3 -I skills/obsidian-project-docs/scripts/validate_vault.py ~/Vaults/Acme
python3 -I skills/obsidian-project-docs/scripts/cobertura_fontes.py /path/to/project ~/Vaults/Acme
```

In a vault whose root has `00 Sistema/projetos.yaml` (a "configured vault"), the skill follows
`references/vault-configurado.md`: the home note is `<Project> Home.md`, every note name gets the
`<Project> - ` prefix, overview/architecture/module notes use `tipo` `visao-geral`/`arquitetura`/`modulo`
so the vault's own tooling (`cerebro conhecimento`) can read them. Pass the vault root and home:

```bash
python3 -I skills/obsidian-project-docs/scripts/validate_vault.py "~/Vault/02 Projetos/Acme" --vault-root ~/Vault --home "Acme Home"
```

## Contributing

Issues and pull requests are welcome. Good contributions: stack-specific investigation hints, new note templates, validator checks, and eval cases showing where the skill falls short. Keep `SKILL.md` lean and put detail in `references/`.

## License

MIT
