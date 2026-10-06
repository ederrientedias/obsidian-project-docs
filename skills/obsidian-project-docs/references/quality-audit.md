# Quality audit

Run this before declaring an area finished (the per-area checks) and before the final report (everything).

## Mechanical checks

When `scripts/validate_vault.py` is available, run it against the docs folder:

```bash
python scripts/validate_vault.py "<path to docs folder>" --vault-root "<path to vault>"
```

It reports broken wikilinks, orphan notes, notes missing frontmatter or required properties, note names that collide with other notes in the vault, empty sections, and strings that look like secrets. Fix everything it reports, or justify what you leave.

Without the script, or when writing through MCP only, do the same by hand:

1. List every note you created.
2. Search the notes for `[[` and confirm each target exists in that list or elsewhere in the vault.
3. Confirm every note except the home note is linked from at least one other note.
4. Confirm each note has frontmatter with `type`, `project`, `status` and `last_reviewed`.
5. Search for patterns that suggest secrets: long random strings, `key=`, `token`, `secret`, `password`, `-----BEGIN`, connection strings with credentials, JWT-like strings starting with `eyJ`.

## Per-area checks

- Responsibilities of each documented thing are clear.
- Flows are complete from trigger to result, including the error path.
- Dependencies and dependents are recorded in both directions.
- Facts, inferences and open questions are visibly distinct.
- No note contradicts another.
- Important claims carry evidence.

## Final questions

Answer each honestly. A "no" means more work or an explicit entry in the coverage note.

1. Is the architecture understandable from the overview alone?
2. Are the main flows documented end to end?
3. Are modules linked to the right pages, entities and integrations?
4. Do data paths have a clear origin and destination?
5. Is every integration documented?
6. Can the design system be understood without opening dozens of files?
7. Are risks and opinions separated from facts?
8. Are unknowns recorded as open questions and nowhere stated as facts?
9. Are the notes connected, with no orphans and no broken links?
10. Is there any contradictory information?
11. Does the coverage note account for every applicable area?
12. Could another agent work on this project using mainly this vault?

Test question 12 concretely: pick two or three realistic tasks (add a field to an entity and show it on its page, find where a business rule is enforced, set up the project locally) and check that the vault alone leads to the right files and steps. Fix what falls short.

## Spot-check accuracy

Pick five to ten claims at random from different notes, weighted toward business rules and data flows, and re-verify each against the code. If more than one is wrong, the affected area needs another pass, because the error rate you sample is the error rate the reader gets.

## Questions the vault must answer

What does the project do? How is it architected? How do I run it? Which modules exist and how does each work? How does data move and where is it stored? Which integrations exist? How does a given page work? Which components exist? How does the design system work? Which code conventions apply? How do authentication and authorization work? How is it deployed? How is it tested? Which risks and tech debt exist? What still needs validation?
