# obsidian-project-docs

An agent skill that investigates a software project end to end and writes a structured, interlinked, evidence-backed knowledge base into an Obsidian vault.

The result is meant to let a developer or an AI agent who has never seen the project understand its architecture and work on it without reading the whole codebase first.

## What it produces

- Overview, tech stack, structure and getting-started notes
- Architecture map with Mermaid diagrams
- One note per module, business flow, page, key component, data entity and integration
- Design system (real tokens, patterns, inconsistencies)
- Data model and data lineage
- Security, performance, testing, CI/CD and environments
- Conventions, runbooks and reconstructed architecture decisions
- Technical debt register with severity
- Open questions for everything that could not be confirmed
- A coverage checklist and a state note that enables incremental updates

## Principles

- **Read-only**: the project is never modified. Only documentation is written.
- **Evidence first**: claims cite the file they come from and are labeled Confirmed, Inferred or Needs validation.
- **No secrets**: variable names and purposes only, never values.
- **Adaptive**: the investigation adapts to the stack (web app, API, mobile, CLI, library, data pipeline, monorepo) and to a depth tier (Survey, Standard, Deep).
- **Plain Obsidian**: wikilinks, properties, callouts and Mermaid. No community plugins required.
- **Language-aware**: the vault is written in the language you talk to the agent in.

## Install

### Claude Code plugin (recommended)

Inside Claude Code:

```text
/plugin marketplace add ederriente/obsidian-project-docs
/plugin install obsidian-project-docs@obsidian-project-docs
```

Update later with `/plugin marketplace update obsidian-project-docs`.

### Claude Code, as a plain skill

```bash
git clone https://github.com/ederriente/obsidian-project-docs /tmp/opd
cp -r /tmp/opd/skills/obsidian-project-docs ~/.claude/skills/
```

Use `.claude/skills/` inside a repository instead of `~/.claude/skills/` to install it for one project only.

### Claude apps

Zip the `skills/obsidian-project-docs` folder and upload it in the skills settings.

## Use

Open the agent in the project you want documented and ask, for example:

```text
Document this project in my Obsidian vault at ~/Vaults/Work, under Projects/Acme CRM.
```

```text
Documenta esse projeto no Obsidian, nível deep, e use o app rodando em localhost:4200 para conferir as telas.
```

```text
The code changed a lot since last month. Update the project docs in Obsidian.
```

The skill detects how to write to the vault: Obsidian MCP tools when present, direct files in the vault folder otherwise, or an output folder you can drop into the vault.

## Layout

```text
.claude-plugin/
  plugin.json                         plugin manifest
  marketplace.json                    lets the repo be added as a marketplace
skills/obsidian-project-docs/
  SKILL.md                            workflow and core rules
  references/
    investigation-playbook.md         what to look for in each area
    vault-structure.md                folders, naming, home and meta notes
    obsidian-conventions.md           frontmatter, links, evidence, diagrams
    note-templates.md                 templates per note type
    quality-audit.md                  audit before finishing
  scripts/
    validate_vault.py                 broken links, orphans, frontmatter, secrets
evals/
  evals.json                          test prompts for iterating on the skill
```

## Validate a generated vault

```bash
python skills/obsidian-project-docs/scripts/validate_vault.py "~/Vaults/Work/Projects/Acme CRM" --vault-root ~/Vaults/Work
```

## Contributing

Issues and pull requests are welcome. Good contributions: stack-specific investigation hints, new note templates, validator checks, and eval cases showing where the skill falls short. Keep `SKILL.md` lean and put detail in `references/`.

## License

MIT
