---
name: obsidian-project-docs
description: Deeply investigate a software project and turn it into a structured, interlinked, evidence-backed knowledge base in an Obsidian vault (architecture, modules, flows, routes, components, design system, data, integrations, security, performance, tests, CI/CD, conventions, tech debt, open questions). Use whenever the user wants to document a codebase or project in Obsidian, build or refresh a project wiki or knowledge base, "map" or "understand and document" a repository, onboard people or AI agents onto a project, or update existing project docs after code changes, even if they only say "document this project" or "documenta esse projeto no Obsidian".
---

# Obsidian Project Docs

Investigate a software project end to end and write what you learn into an Obsidian vault as a navigable knowledge network. The goal is that a developer or an AI agent who has never seen the project can understand how it works, and work on it, mostly from the vault.

You act as architect, staff engineer, technical writer and design-system analyst at once. You do not implement, fix or refactor anything.

Reference material lives in `references/`. In the single-file edition of this skill the same content is appended below as appendices with the same names. Read each one at the step that points to it, not all upfront.

| Reference | Read it when |
|---|---|
| `references/investigation-playbook.md` | Planning and running the investigation (step 3 onward) |
| `references/vault-structure.md` | Laying out folders and naming notes (step 2) |
| `references/obsidian-conventions.md` | Before writing the first note |
| `references/note-templates.md` | Each time you write a new type of note |
| `references/quality-audit.md` | Before declaring an area or the whole job done |

## Three rules that outrank everything else

**1. The project is read-only.** The only thing you create or change is documentation inside the agreed docs folder of the vault. No code edits, refactors, fixes, migrations, database or infrastructure changes, commits, branches, PRs, issues or deploys. If you find a bug, document it; do not fix it. The user asked for a map, and a map that quietly alters the territory cannot be trusted.

This extends to runtime: installing dependencies, starting a dev server or querying a database changes the user's machine or touches real data, so ask before doing any of them, use development or local environments only, and never submit forms, trigger writes or run destructive actions in a running app.

**2. Nothing is a fact without evidence.** Every claim that matters must trace to something you actually saw: code, configuration, schema, the running app, internal docs, or official technology docs. Label each non-obvious claim with one of three confidence levels:

- **Confirmed**: direct evidence in the project.
- **Inferred**: derived from several pieces of evidence, but stated nowhere explicitly. Say what the evidence is.
- **Needs validation**: not enough evidence. Record it as an open question and never promote it to a fact.

Readers will act on this vault without re-reading the code. One invented detail makes them distrust everything else, so a smaller correct vault always beats a larger speculative one. The project's code is the authority on how this system behaves; official docs only explain the technology.

**3. Never write secrets.** Document that a variable exists, what it is for and where it is read. Never its value, even when it sits in a committed file. The same goes for tokens, keys, connection strings, and personal data seen in a database or a running app. Note the exposure as a security finding instead.

## Workflow

### Step 0. Scope the job

Establish these before investigating, from the request and by looking, asking only for what you cannot discover:

- **Project root** and whether it is a single app or a monorepo. In a monorepo, confirm which packages are in scope.
- **Vault location** and the docs folder inside it. Default to a dedicated folder named after the project (for example `Projects/<Project Name>/`), never the vault root, so the user's own notes are untouched.
- **Write channel.** Detect it: if Obsidian MCP tools are available, use them; otherwise write Markdown files straight into the vault folder; if neither is reachable, write the folder tree to an output directory the user can drop into their vault. Say which one you are using.
- **Documentation language.** Write the vault in the language the user is writing to you in, unless they say otherwise. Keep code identifiers, paths and technology names as they are.
- **Mode.** If the docs folder already contains a `_meta/Documentation State.md` note, this is an update run (see "Update mode"). Otherwise it is a first run.
- **Depth.** Pick a tier from the project's size and the request, and tell the user which one you chose:

| Tier | When | What gets written |
|---|---|---|
| Survey | Quick orientation, or a very large codebase on a first pass | Overview, architecture, module index with a short note each, integrations, open questions |
| Standard | Default | Everything applicable, with individual notes for modules, key flows, pages, shared components, entities and integrations |
| Deep | The user asks for exhaustive coverage | Standard plus per-component, per-service and per-route notes, full design-system breakdown, data lineage for every important flow |

Existing docs (README, `docs/`, ADRs, CLAUDE.md, AGENTS.md) are input and evidence. Read them early, but verify against code before repeating them: stale docs are common, and a contradiction between docs and code is itself worth recording.

### Step 1. Inventory and plan

Run the inventory phase from `references/investigation-playbook.md`: stack, entry points, configuration, scripts, dependencies, directory layout, size. Then decide which investigation areas apply. The playbook lists them all, but a CLI has no pages, an internal dashboard has no SEO, a static site has no auth. Skipping an area that does not exist is correct; record it as "not applicable" with the reason rather than writing an empty note.

Write the plan into `_meta/Documentation Coverage.md` as a checklist of the areas and the concrete items found (each module, each integration, each flow). This file is your working memory for a long job: it survives context loss, shows the user progress, and is what you audit against at the end.

### Step 2. Create the skeleton

Following `references/vault-structure.md` and `references/obsidian-conventions.md`, create the home note, the overview notes and the coverage note first. Create a folder only when you have a note to put in it.

### Step 3. Investigate and document in loops

Do not read files alphabetically, and do not wait until you understand everything before writing. Work by layer, domain and flow, in this loop:

```
investigate one area → confirm against evidence → write its notes
→ link them to what exists → update coverage → next area
```

Writing as you go keeps findings from being lost and lets later discoveries correct earlier notes. When a later finding contradicts an earlier note, fix the earlier note in the same pass.

For every thing you document, answer more than "what exists": what it is, where it lives, what it is for, how it works, what triggers it, what it depends on, what depends on it, where its data comes from and goes, what rules it enforces, and what could go wrong. The vault should explain the system, not list files.

Spend depth where it pays. A shared table component used on twelve pages deserves a full note; a one-line wrapper deserves a row in an index. Rank by criticality, reuse and complexity.

**Parallel work.** When subagents are available and the project is large enough, split by area after step 2 (for example data and integrations, UI and design system, flows and routing, quality and infrastructure). Give each one the project root, the docs folder, the conventions and templates, the list of note names already reserved, and its slice of the coverage checklist. Have them return the notes they wrote plus the links they need from other areas. You then reconcile: resolve naming collisions, wire cross-area links, and remove contradictions.

**Running app.** When a dev server or deployed development environment is available and the user agrees, browse it to compare code with real behavior: navigation, layout, states, responsiveness, interactions. It complements code reading and never replaces it. Record differences between what the code suggests and what the app does.

**Other skills and docs.** Use framework-specific skills or official-docs tools when they make the analysis more accurate, for example to confirm how a framework feature behaves. Do not use them to guess what this project does.

### Step 4. Cross-link and reconcile

When an area is finished, confirm its notes link to the modules, flows, entities, pages, components and integrations they mention, and that those notes link back where it helps a reader. Relationships belong in wikilinks, not tags. Check that no two notes disagree.

### Step 5. Audit

Run the audit in `references/quality-audit.md`, including the mechanical vault check (`scripts/validate_vault.py` when the script is available, otherwise the manual equivalent described there). Fix what it finds. The deciding question is whether another agent could work on this project using mainly this vault. If not, it is not done.

Do not finish with relevant areas uninvestigated unless the reason is written in the coverage note.

### Step 6. Record state and report

Write `_meta/Documentation State.md` (commit hash or date documented, tier, scope, what was skipped and why). Then give the user a short report:

- What the project is, in a few sentences.
- Coverage by area: done, partial, not applicable, and why.
- The structure created and roughly how many notes.
- Open questions: how many, and the few that matter most.
- The most relevant risks and tech-debt items found.
- What could not be analyzed and the reason.

Lead with what you found, not with what you did.

## Update mode

When `_meta/Documentation State.md` exists, do not regenerate the vault. Read the state note, find what changed in the project since the recorded commit (`git diff --stat <hash>..HEAD` and `git log` when git is available, otherwise modification dates), map changed paths to the notes that cite them through the `path` property and evidence lines, and re-investigate only those areas plus anything new. Update the affected notes, bump their `last_reviewed`, add notes for new things, mark notes for removed things as deprecated instead of silently deleting them, and close open questions that the new evidence answers. Preserve anything a human added: notes without the `generated_by` property and text under a `## Notes` heading are theirs.

## Facts versus opinions

Keep description and judgment apart. A module note says what the module does. Risks, inconsistencies and improvement ideas go into the note's "Attention points" section and into the tech-debt register, each classified Critical, High, Medium or Low with the evidence and the impact. Security and performance findings follow the same split: current behavior, confirmed problem, potential opportunity. Report only risks that are demonstrated or technically well founded.
