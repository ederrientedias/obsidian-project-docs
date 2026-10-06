# Vault structure

Everything lives under one docs folder for the project (for example `Projects/Acme CRM/`). Use the layout below as a starting point and adapt it to the real project. Create a folder only when it will hold a note. Folder and note names follow the documentation language; the English names here are the default.

```text
<Project>/
  <Project> Home.md                 entry point and map of content
  Start Here for AI Agents.md       how an agent should use this vault
  00 Overview/
    Project Overview.md
    Tech Stack.md
    Project Structure.md
    Getting Started.md
  01 Architecture/
    Architecture Overview.md
    Routing and Navigation.md
    State Management.md
    Data Flow.md
    Decisions/                      Decision - <topic>.md
  02 Modules/                       Module - <name>.md
  03 Flows/                         Flow - <name>.md
  04 Pages/                         Page - <name>.md
  05 Components/
    Components Overview.md          index table of all components
    Component - <name>.md           only for components that deserve a note
  06 Design System/
    Design System Overview.md
    Colors.md  Typography.md  Spacing and Layout.md  UI Patterns.md
  07 Data/
    Data Model.md
    Entity - <name>.md
    Data Lineage.md
  08 Integrations/                  Integration - <name>.md
  09 Services and APIs/             Service - <name>.md, API Reference.md
  10 Security/                      Security Overview.md, Authentication and Authorization.md
  11 Performance/                   Performance Overview.md
  12 Testing/                       Testing Strategy.md
  13 Infrastructure/                Environments.md, CI-CD and Deploy.md
  14 Engineering Standards/         Conventions.md, Runbook - <task>.md
  15 Technical Debt/                Technical Debt Register.md
  16 Glossary/                      Glossary.md
  99 Open Questions/                Open Questions.md
  _meta/
    Documentation Coverage.md
    Documentation State.md
```

Modules and features: if the project distinguishes them, split into two folders. If it does not, keep one folder and use the project's own word.

## Naming notes

Obsidian resolves `[[Name]]` across the whole vault, so a note named `Button` or `Supabase` can collide with the user's other notes or with another documented project. Avoid that:

- Prefix typed notes with their type: `Module - Contacts`, `Flow - Create Contact`, `Page - Contact Detail`, `Component - DataTable`, `Entity - contacts`, `Integration - Supabase`, `Service - contacts.service`, `Decision - Server state with React Query`, `Runbook - Add a new page`.
- For generic titles that every project has (`Architecture Overview`, `Glossary`, `Tech Stack`), check whether the vault already contains a note with that name. If it does, or if the vault holds several projects, prefix with the project name (`Acme CRM - Glossary`).
- Add the short name as an `aliases` entry so the note is still easy to find, and link with display text for readability: `[[Module - Contacts|Contacts]]`.
- Do not use `* " \ / < > : | ? # ^ [ ]` in file names. They are either invalid on some systems or break links.
- Keep a list of the names you have used. Reusing a name for a second note is the most common cause of wrong links.

## The home note

`<Project> Home.md` is a map of content: one paragraph on what the project is, then links to each area's overview note, the key flows, the open questions and the tech-debt register. Area overview notes act as the next level of map. A reader should reach any note in three clicks from home.

## Start Here for AI Agents

A short note that tells an agent how to use the vault:

- What the project is and where the code lives.
- Reading order for a new task: home → architecture overview → the module note → its flows and entities.
- How to interpret confidence labels and evidence lines.
- Where conventions and runbooks are, so new code follows existing patterns.
- That open questions are unknowns, not facts.
- The commit and date the vault reflects, with a warning to verify against code when the code is newer.

## The _meta folder

- `Documentation Coverage.md`: the checklist of areas and concrete items, with status (done, partial, not applicable, pending) and a reason for anything not done.
- `Documentation State.md`: project path, commit hash and date documented, depth tier, scope, write channel used, date of the run. Update mode depends on it.
