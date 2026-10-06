# Obsidian conventions

Use only core Obsidian features so the vault works for anyone with no plugins installed. Do not depend on Dataview, Templater or other community plugins. If the user already uses one, you may add an optional query block, but the note must stay complete without it.

## Writing channel

- **Obsidian MCP tools available**: use them to list, read, create and patch notes. Paths are relative to the vault root. Read a note before overwriting it.
- **Direct file access**: write `.md` files into the vault folder. Obsidian picks them up automatically. Do not touch the `.obsidian/` folder.
- **Neither**: write the folder tree to an output directory and tell the user to move it into their vault.

Before writing into an existing folder, list what is there. Never overwrite or delete a note you did not generate (no `generated_by` property) without asking.

## Frontmatter (properties)

Every generated note starts with YAML frontmatter. Keep the property set small and consistent, because inconsistent properties are useless for filtering.

```yaml
---
type: module            # overview | architecture | module | flow | page | component | design-system | entity | integration | service | security | performance | testing | infrastructure | standard | runbook | decision | tech-debt | glossary | open-questions | meta
project: Acme CRM
status: documented      # documented | partial | needs-validation | deprecated
confidence: confirmed   # confirmed | inferred | mixed
path: src/features/contacts      # main source location, when one exists
aliases:
  - Contacts
tags:
  - acme-crm/module
last_reviewed: 2026-01-15
source_commit: a1b2c3d
generated_by: obsidian-project-docs
---
```

Rules:

- `aliases` and `tags` are lists. Dates are `YYYY-MM-DD`.
- Do not put wikilinks in frontmatter except in a dedicated list property such as `related`, quoted: `related: ["[[Flow - Create Contact]]"]`. Relationships mainly belong in the body.
- Omit a property that has no value. Do not add properties nobody will filter on.

## Links

- Use wikilinks for every relationship: `[[Module - Contacts]]`, with display text when it reads better: `[[Module - Contacts|Contacts]]`. Link to a section with `[[Note#Heading]]`.
- Link the first meaningful mention in each section, not every occurrence.
- Each typed note ends with a `## Related` section listing the modules, flows, pages, components, entities and integrations it touches. This gives the reader a way out and makes backlinks meaningful.
- Only link to notes that exist or that you will create in this run. A link to a note you never write is a broken promise; the audit catches these.
- Link to code with the relative path in backticks, not with a wikilink.

## Tags

Use few, and only for cross-cutting classification that links cannot express. Nest them under the project so they do not pollute the user's tag list: `#acme-crm/module`, `#acme-crm/risk/high`, `#acme-crm/needs-validation`. Note type already lives in the `type` property.

## Evidence and confidence

Cite the origin of important claims right where they are made:

```markdown
Contacts are soft-deleted: `deleted_at` is set and every read filters on it.
Evidence: `src/features/contacts/contacts.service.ts:42-58`, `supabase/migrations/0007_contacts.sql:12`
```

Use `path:line` or a line range when it is stable enough to help, and the file path alone otherwise. Cite decisions, rules, data flows and anything surprising. Do not turn notes into path dumps.

Use callouts for anything that is not confirmed, so it stands out visually:

```markdown
> [!info] Inferred
> The module seems to be mid-migration from Redux to React Query: new files use query hooks, older ones still dispatch actions.
> Evidence: `src/features/orders/hooks/`, `src/features/orders/store/`

> [!question] Needs validation
> No evidence of who triggers the nightly export. See [[Open Questions#Q-004]].

> [!warning] Risk (High)
> The admin route has no guard. Evidence: `src/app/app.routes.ts:88`
```

Plain text needs no label: unlabeled statements are confirmed by the evidence cited near them.

## Diagrams

Use Mermaid, which Obsidian renders natively, when a picture explains something faster than text:

| Subject | Diagram |
|---|---|
| Layers, module dependencies, navigation | `flowchart` |
| A flow across components over time | `sequenceDiagram` |
| Data model | `erDiagram` |
| Lifecycles and status machines | `stateDiagram-v2` |

Keep each diagram under roughly fifteen nodes and split larger ones. Quote labels that contain punctuation (`A["contacts.service"]`). Every node must correspond to something real in the project. No decorative diagrams.

## Writing style

- Start each note with one or two sentences that say what the thing is and why it exists.
- Prefer prose for explanations and tables for enumerable facts (routes, props, fields, endpoints, env variables).
- Leave out template sections that do not apply instead of writing "N/A" in them.
- Short code excerpts are welcome when they are the evidence for a rule. Do not paste whole files.
- Write for a reader who has not seen the code and does not know the internal jargon. Define terms or link to the glossary.
