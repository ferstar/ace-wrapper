# AI Agent Prompt Guidance

To use `ace` effectively with AI coding agents (like Antigravity, Claude Engineer, or Cursor), you can include the following instructions in your project's agent configuration files (e.g., `.cursorrules`, `CLAUDE.md`, `GEMINI.md`, or `AGENTS.md`).

## Recommended Prompt Snippet

```markdown
### ACE Semantic Search
- Use `ace` for intent-based or open-ended codebase search: `timeout 60s ace "query" -w <repo-root>`.
- If you do not know the exact keywords (debugging, explorations, "where is X?"), run `ace` before `rg`.
- Treat `ace` as a candidate-file generator, not a proof source. After it returns results, read the relevant files and use exact search to confirm identifiers or call sites.
- Split unrelated questions into separate `ace` queries.
- Do not treat "results found" as evidence that a feature exists. Verify existence from code before concluding.
- Prefer queries that describe behavior and data flow, not just nouns: include user action, runtime boundary, expected effect, and any known payload fields.
```

## Best Practices

1. **Start with Intent**: Don't just search for "login", search for "how the user is authenticated and session is created".
2. **Context is Key**: Include the runtime boundary (e.g., "from UI to backend") to help the engine find the right layer.
3. **Verify Everything**: Always follow up an `ace` search with `grep` or file reads to confirm the findings.
