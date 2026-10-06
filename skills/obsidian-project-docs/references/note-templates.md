# Note templates

Starting shapes for each note type. Translate headings to the documentation language. Drop sections that do not apply and add ones the project needs. All notes begin with the frontmatter described in the Obsidian conventions and end with `## Related`.

## Module or feature

```markdown
# Module - <Name>

<What it is and which problem or domain it covers, in one or two sentences.>

## Location
## Responsibilities
## Structure
<Relevant folders and files with the role of each.>
## How it works
<Input: what triggers it. Processing: what happens inside. Output: what it produces or changes.>
## Business rules
<Each rule in plain language with its evidence.>
## Data
<What it reads and writes; links to entities.>
## Types and contracts
## Dependencies
## Dependents
## Integrations
## Error handling
## Performance
## Security
## Tests
## Attention points
<Risks and inconsistencies, each with severity and evidence.>
## Related
```

## Flow

```markdown
# Flow - <Name>

<What the user or system achieves with this flow.>

## Trigger
## Preconditions
## Steps
<Numbered. Each step names the file or component responsible.>
## Diagram
<sequenceDiagram>
## Data and persistence
## Integrations
## Error paths
## Result
## Related
```

## Page

```markdown
# Page - <Name>

## Purpose
## Route
<URL, layout, auth and permissions, parameters.>
## Visual structure
## Components
## Data
## User actions
## States
<Loading, empty, error, success.>
## Responsiveness
## Accessibility
## Related
```

## Component

```markdown
# Component - <Name>

## Responsibility
## Location
## API
<Table: prop or input, type, default, purpose. Events or outputs.>
## Variants and visual states
## Internal state and behavior
## Dependencies
## Accessibility
## Used in
## Attention points
## Related
```

## Entity

```markdown
# Entity - <name>

<What it represents in the domain.>

## Defined in
## Fields
<Table: field, type, constraints, meaning.>
## Relationships
## Access rules
## Written by
## Read by
## Transformations
## Related
```

## Integration

```markdown
# Integration - <Name>

## Purpose
## Configuration
<Config files and environment variable names. No values.>
## Client and authentication
## Where it is used
## Data sent
## Data received
## Error handling
## Risks
## Related
```

## Service or API

```markdown
# Service - <name>

## Responsibility
## Location
## Operations
<Table: operation, input, output, what it calls.>
## Dependencies
## Error handling
## Consumers
## Related
```

## Decision

```markdown
# Decision - <Topic>

## Context
## Decision
## Evidence
## Rationale
<Stated in the project, or "not documented" with the inferred reason marked as inferred.>
## Consequences
## Related
```

## Runbook

```markdown
# Runbook - <Task>

## When to use
## Prerequisites
## Steps
<Verified from scripts and config; cite them.>
## Verify
## Related
```

## Technical debt register

One note with a summary table, then one section per item.

```markdown
| ID | Item | Severity | Area | Evidence |
|---|---|---|---|---|
| TD-001 | Two competing table components | Medium | [[Components Overview]] | `src/components/Table`, `src/shared/DataTable` |

## TD-001 - Two competing table components
Severity: Medium
What: ...
Evidence: ...
Impact: ...
Suggested direction (opinion): ...
```

## Open questions

```markdown
## Q-001 - <Short description>
Context:
Evidence found:
What could not be confirmed:
Impact:
Where to validate: <person, system or file likely to hold the answer>
Status: open
```

## Documentation coverage

```markdown
## Architecture
- [x] Overall structure
- [x] Routing
- [ ] State management (pending)

## Modules
- [x] Contacts
- [~] Mailing (partial: sending pipeline not traced; see Q-003)

## Not applicable
- SEO: internal application behind login
```

## Documentation state

```markdown
- Project path:
- Scope:
- Source commit:
- Documented on:
- Depth tier:
- Write channel:
- Skipped areas and reasons:
```
