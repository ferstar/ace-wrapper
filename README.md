# ACE Wrapper

Semantic codebase retrieval using the Augment Context Engine through a small `ace` command.

Use it when the relevant identifiers are unknown and the query is about behavior, intent, architecture, or data flow. Treat results as candidate files, then read the returned files and confirm exact identifiers or call sites with literal search.

## Prerequisites

Authenticate the Augment CLI before searching:

```bash
auggie login
```

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

## Reliability Boundaries

- ACE is a candidate-file generator, not proof that a feature exists.
- Verify important conclusions by reading files and using exact search.
- Split unrelated workflows into separate queries.
- Use literal search for exact identifiers, error strings, routes, events, and config keys.

More usage guidance lives in [references/guide.md](references/guide.md).
