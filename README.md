# ACE Wrapper

Semantic codebase retrieval using the Augment Context Engine through a small `ace` command.

Use it when the relevant identifiers are unknown and the query is about behavior, intent, architecture, or data flow. Treat results as candidate files, then read the returned files and confirm exact identifiers or call sites with literal search.

## Authentication

Before searching, you must authenticate using **one** of the following methods:

### Method 1: Standard Login (Official)

If you have an official Augment account:

```bash
auggie login
```

### Method 2: ACE Relay (Alternative)

If you use an `ace relay` middleman service, you can **skip** `auggie login` by manually configuring `~/.augment/session.json` with relay-specific settings:

- `accessToken`: Use the relay token (e.g., starts with `ace_`).
- `tenantURL`: Change to the relay endpoint (e.g., `https://acemcp.heroman.wtf/relay/`).
- `scopes`: Typically set to `["email"]`.

## Install

From this repository:

```bash
uv tool install .
```

From a published package:

```bash
uv tool install ace-wrapper
```

## Usage

```bash
timeout 60s ace "How is the authentication flow implemented?" -w /path/to/project/root
timeout 60s ace "Find where uploaded files are validated and stored" -w /path/to/project/root
timeout 60s ace "用户登录流程在哪里实现" -w /path/to/project/root
```

Use `--verbose` for debug logs:

```bash
timeout 60s ace "config loading" -w /path/to/project/root --verbose
```


## AI Agent Integration

To use `ace` effectively with AI coding agents, add the following guidance to your agent's prompt instructions (e.g., in `.cursorrules`, `CLAUDE.md`, or `GEMINI.md`):

```markdown
### ACE Semantic Search
- Use `ace` for intent-based or open-ended codebase search: `timeout 60s ace "query" -w <repo-root>`.
- If you do not know the exact keywords (debugging, explorations, "where is X?"), run `ace` before `rg`.
- Treat `ace` as a candidate-file generator, not a proof source. After it returns results, read the relevant files and use exact search to confirm identifiers or call sites.
- Split unrelated questions into separate `ace` queries.
- Do not treat "results found" as evidence that a feature exists. Verify existence from the code before concluding.
- Prefer queries that describe behavior and data flow, not just nouns: include user action, runtime boundary, expected effect, and any known payload fields.
```

## Reliability Boundaries

- ACE is a candidate-file generator, not proof that a feature exists.
- Verify important conclusions by reading files and using exact search.
- Split unrelated workflows into separate queries.
- Use literal search for exact identifiers, error strings, routes, events, and config keys.

More usage guidance lives in [references/guide.md](references/guide.md).

## Release

Publishing is handled by GitHub Actions. Create and push a version tag to build, publish to PyPI, and create a GitHub Release:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The PyPI publish job uses Trusted Publishing, so the PyPI project must allow the `ferstar/ace-wrapper` repository and the `pypi` GitHub environment.
