---
name: ace-wrapper
description: |
  Semantic codebase retrieval using Augment SDK / ACE. Use it before literal grep when the user describes behavior, intent, architecture, data flow, or an implementation whose exact identifiers are unknown. Treat results as candidate files, then verify with file reads and exact search. Triggers: semantic search, ace, augment context, code search, find implementation, architectural context, 搜索代码, 语义搜索, 代码库检索, 查找实现, 逻辑分析, 架构理解.
---

# Augment Context Engine (ACE) Wrapper

Semantic search for finding code by behavior, intent, and architecture when exact keywords are unknown.

## Prerequisites

Before using this skill, ensure the Augment CLI is authenticated on the machine where the agent runs:

```bash
auggie login
```

## Install for AI Coding Agents

Install the wrapper as a global tool so any coding agent can call `ace` from its shell:

```bash
uv tool install ace-wrapper
```

For local development or unpublished checkouts:

```bash
uv tool install /path/to/ace-wrapper
```

Agent instruction snippet:

```markdown
### ACE Semantic Search
- Use `ace` for intent-based or open-ended codebase search: `timeout 60s ace "query" -w <repo-root>`.
- If you do not know the exact keywords (debugging, explorations, "where is X?"), run `ace` before `rg`.
- Treat `ace` as a candidate-file generator, not a proof source. After it returns results, read the relevant files and use exact search to confirm identifiers or call sites.
- Split unrelated questions into separate `ace` queries.
- Do not treat "results found" as evidence that a feature exists. Verify existence from code before concluding.
- Prefer queries that describe behavior and data flow, not just nouns: include user action, runtime boundary, expected effect, and any known payload fields.
```

## Quick Reference

| Action | Command |
| :--- | :--- |
| Search current directory | `timeout 60s ace "<query>"` |
| Search specific project root | `timeout 60s ace "<query>" -w <path_to_root>` |
| Debug mode | `timeout 60s ace "<query>" -w <path_to_root> --verbose` |

Note: Semantic search may take longer than literal search; always use an explicit timeout when calling from agents or scripts.

## When to Use This Skill

**Use ACE (Semantic Search) when:**
- **Searching for concepts** ("auth flow", "data persistence") rather than exact strings
- Exploring unfamiliar architecture or cross-file dependencies
- Translating natural language intents (e.g., Chinese queries for English code)
- Understanding how features are implemented across multiple files
- Debugging from symptoms when the relevant function, event, or file name is unknown
- Tracing a workflow across UI, IPC/API, backend/core, tests, and docs

**Fall back to Grep when:**
- Seeking **exact identifiers** (`grep "UserRepository"`)
- Searching for literal error messages or config constants
- Performing bulk refactoring and needing every occurrence
- Confirming exact call sites after ACE returns candidate files

## Workflow Integration

To investigate code effectively:

1. Read nearby project guidance if the repository has it.
2. Use `ace` to find candidate files and functions for open-ended questions.
3. Read the most relevant returned files before drawing conclusions.
4. Use exact search (`grep`/`rg`) to confirm identifiers, event names, tests, call sites, or every occurrence.
5. If results are weak, retry with a different behavior/data-flow query, then use exact search as fallback.

For agent prompt files such as `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`, keep the rule short: run ACE for open-ended code discovery, verify by reading files, and use exact search for proof.

## Query Guidance

- Prefer behavior and data flow over nouns only: include the user action, runtime boundary, expected effect, and known payload fields.
- Keep one workflow or concept per query. Split unrelated questions into separate `ace` calls; multi-topic queries can miss weaker subtopics.
- Long natural-language queries are fine when they describe one coherent workflow.
- For negative checks ("does this feature exist?"), do not trust `ace` alone.

## Reliability Boundaries

- ACE is a candidate-file generator, not a proof source.
- A result means "semantically nearby", not "the feature definitely exists".
- Fictional or negative queries may still return approximate matches. Verify existence from code before concluding.
- Exact identifiers, error strings, API paths, and config keys are usually better handled by literal search.

## Reference Materials

- `references/guide.md` - Detailed usage patterns and troubleshooting
- [Official SDK Docs](https://docs.augmentcode.com/context-services/sdk/overview#filesystem-context)
