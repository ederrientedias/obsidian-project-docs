# Investigation playbook

What to look for in each area. Areas are ordered so that each one gives context to the next, but treat the order as a default, not a law. Skip areas that do not exist in the project and say so in the coverage note.

Contents: 1 Inventory · 2 Architecture map · 3 Modules and features · 4 Flows · 5 Routes and navigation · 6 Components · 7 Design system · 8 Pages and layouts · 9 Data model · 10 Data lineage · 11 Integrations · 12 State · 13 Reusable logic · 14 Services and APIs · 15 Security · 16 Performance · 17 SEO · 18 Tests · 19 CI/CD and environments · 20 Conventions · 21 Tech debt · 22 Decisions · 23 Runbooks · 24 Glossary · Stack adaptation

The lists use frontend-heavy vocabulary because that is the common case. Translate to the stack in front of you (see "Stack adaptation" at the end).

## 1. Inventory

Establish the ground truth before any deep reading.

- Languages, frameworks and their versions, package manager, build system, runtime versions.
- Manifest and lock files, build and bundler config, compiler config, lint and format config, styling config, framework config, backend-platform config, container and infrastructure files.
- Scripts and what each one really runs.
- Entry points and bootstrap sequence.
- Directory layout, with the purpose of each top-level folder.
- Environment variables: names, purpose, where they are read. Never values.
- Main dependencies grouped by role (UI, data, state, auth, testing, tooling), and notably outdated or duplicated ones.
- External services the project talks to.
- Size: file and line counts per area, to choose the depth tier and spot where the weight is.
- Monorepo: workspaces, their relationships, shared packages.

Output: overview, tech stack, project structure, getting started.

## 2. Architecture map

Discover the architecture the project really uses. Do not impose a textbook one. If the code is half feature-sliced and half layered, say that.

Identify the layers and building blocks present (features, modules, pages, components, shared, UI kit, hooks or composables, services, repositories, contexts, stores, utils, types, schemas, API handlers, jobs, events, infrastructure) and how they are allowed to depend on each other in practice. Note boundaries that are respected and ones that are violated.

Output: architecture overview with a layer diagram and a module dependency diagram.

## 3. Modules and features

For each module or feature: name, location, the domain or problem it represents, responsibilities, internal structure, how it is triggered (input), what happens inside (processing), what it produces or changes (output), dependencies, dependents, data read and written, integrations, business rules found in code, types and contracts, error handling, performance and security aspects, tests, attention points.

Business rules are the most valuable and least visible part. Look for them in validation schemas, conditionals in services and handlers, database constraints and policies, guards, and computed values. Quote the rule in plain language and cite where it lives.

## 4. Flows

Identify the main business flows (sign in, create X, checkout, import, publish) and document each one end to end across files, for example user → page → component → hook → service → API → database → response → UI update.

For each flow: trigger, preconditions, numbered steps with the file responsible for each, components involved, data used, persistence, integrations, error paths, final result. A sequence diagram is usually the right picture.

Flows are what turn a list of files into an explanation. Prioritize them.

## 5. Routes and navigation

Every route: URL pattern, page or handler, layout, owning feature, auth requirement, permissions or roles, path and query parameters, child routes, how users get in and where they go next, lazy loading, guards, resolvers, redirects.

Output: a route table and a navigation map diagram.

## 6. Components

Start with global folders (`components`, `shared/components`, `ui`, design-system packages), then feature-local ones.

For each important component: responsibility, inputs or props, internal state, events or outputs, dependencies, children, parents, reusable logic it uses, variants, visual states, responsiveness, accessibility, where it is used.

Trivial components go in an index table (name, path, one-line purpose, usage count), not individual notes.

## 7. Design system

Document tokens that really exist, from theme files, CSS variables, the styling framework config and component-library config. Do not invent a tidy token system the project does not have.

- Color: semantic roles (primary, secondary, background, surface, border, text, muted, success, warning, error) mapped to real token names and values, light and dark themes.
- Typography: families, weights, scale, heading, body, label and caption styles.
- Spacing scale, radius, borders, shadows, breakpoints, containers, grid, z-index, motion.
- Icons: library and usage pattern.
- Component patterns: buttons, inputs, cards, tables, badges, modals, dropdowns, tabs, sidebar, header, with variants and states.
- Feedback states: loading, empty, error, success, disabled.
- Hardcoded values that bypass tokens, and inconsistencies between screens. Record these separately from the description of the system.

## 8. Pages and layouts

For each relevant page: purpose, route, layout, visual hierarchy, components, data shown, user actions, flows it participates in, states, responsiveness, accessibility, integrations, dependencies. Compare with the running app when available.

## 9. Data model

Databases, schemas, tables, views, collections, documents, storage buckets, caches, search indexes, API resources.

For each relevant entity: name, where it is defined, relevant fields with types and meaning, relationships, constraints and indexes, access policies, who reads it, who writes it, transformations applied on the way in and out. An ER diagram for the core entities.

Sources of truth, in order of reliability: migrations and schema files, generated types, ORM models, security rules and policies, then queries in code. If you can only see the model through usage in code, say it is inferred.

## 10. Data lineage

For important data, trace origin to destination, for example `contacts` table → contacts service → `useContacts` → contacts table component → contacts page. Include mappers and transformations, caching layers, and where the shape changes.

## 11. Integrations

One note per external service or internal platform: purpose, configuration, client or SDK, authentication method, where it is used, data sent, data received, error handling, rate limits and retries, webhooks, dependencies, risks. Variable names only, no secrets.

## 12. State

Where each kind of state lives (local, context, store, server cache, signals, observables, URL, browser storage), who writes it, who reads it, how it syncs with the server, cache invalidation rules, persistence across reloads.

## 13. Reusable logic

Custom hooks, composables, directives, pipes, mixins, shared utilities. For each relevant one: purpose, inputs, outputs, dependencies, state, side effects, where it is used.

## 14. Services and APIs

For each relevant service, repository, API handler, server function, job or event handler: responsibility, operations, inputs, outputs, dependencies, what it calls, error handling, consumers. For an HTTP API, a table of endpoints with method, path, auth, request and response shape.

## 15. Security

Authentication, session handling, authorization, roles, guards, row-level or document-level rules and policies, input validation, output sanitization, secret handling, environment variables exposed to the client, uploads, CORS, API protection, dependency vulnerabilities reported by existing tooling.

Describe how auth works end to end as a flow. List only risks that are demonstrated or technically well founded, each with its evidence.

## 16. Performance

Rendering strategy, re-render hot spots, lazy loading, code splitting, queries, caching, request waterfalls, assets, images, fonts, bundle composition, pagination, large lists, database indexes, N+1 patterns.

Separate three things: current behavior, confirmed bottleneck, potential opportunity. Without measurement, a suspicion is an opportunity, not a bottleneck.

## 17. SEO (public-facing web only)

Metadata, titles, descriptions, canonical, Open Graph, sitemap, robots, structured data, heading structure, semantic markup, image handling, rendering strategy as it affects crawling.

## 18. Tests

Unit, integration, end-to-end and component tests: tools, where they live, how to run them, which features are covered, apparent coverage, important gaps, flaky or skipped tests.

## 19. CI/CD and environments

Build, pipelines, workflows, hosting, environments, release process, secrets management approach, database migration process. Document the flow that is really configured (branch → PR → CI → staging → validation → production) and do not add steps that are not in the configuration. Things that probably happen manually are open questions.

## 20. Conventions

Observed patterns, even when unwritten: naming of files, components, functions and types, folder structure, how components are split, import order and aliases, error-handling style, commit and branch conventions (from git history). Include one real example of each, and note where the code departs from its own conventions.

## 21. Tech debt and inconsistencies

Duplicated code and components, inconsistent structures, scattered types, competing patterns for the same job, dead code, outdated dependencies, bottlenecks, architectural risks, `TODO` and `FIXME` comments with substance. Each item: severity (Critical, High, Medium, Low), evidence, impact, and optionally a suggested direction clearly marked as a suggestion.

## 22. Decisions

Architectural decisions that can be reconstructed from evidence (why this state library, why this data-access pattern, why this folder layout). Mark each as Confirmed when a doc, comment or commit message states it, Inferred otherwise, with the evidence. Never invent a rationale: "reason not documented" is a valid entry and belongs in open questions too.

## 23. Runbooks

Practical how-tos derived from the code and config: set up and run locally, run tests, add a new page or feature following existing patterns, add a new entity or migration, deploy. These make the vault usable, not just descriptive. Only include steps you verified from scripts and config.

## 24. Glossary

Domain terms, internal names and abbreviations found in code and UI, each with a one-line meaning and a link to the note where it matters. Terms whose meaning you could not determine go to open questions.

## Stack adaptation

Map the vocabulary above to the project type and drop what does not apply.

| Project type | Emphasize | Usually not applicable |
|---|---|---|
| SPA or SSR web app | Routes, pages, components, design system, state, flows | Depends on visibility for SEO |
| Angular | Modules or standalone components, services and DI, guards, resolvers, interceptors, signals and RxJS, pipes and directives | "Hooks" (use services, signals, pipes) |
| Backend API or service | Endpoints, domain model, persistence, jobs, events, auth, observability, error contracts | Pages, design system, SEO |
| Mobile app | Screens, navigation stack, native modules, offline and sync, permissions, release channels | SEO |
| CLI or library | Commands or public API surface, options, extension points, versioning, packaging, examples | Routes, pages, design system |
| Data or ML pipeline | Sources, transformations, schedules, lineage, data quality checks, model artifacts | Components, design system, SEO |
| Infrastructure repo | Resources, environments, modules, state management, deployment order, blast radius | UI areas |
| Monorepo | A top-level map of packages and dependencies, then one documentation subtree per app or package | Decide per package |
