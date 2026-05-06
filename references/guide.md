# Augment Context Engine (ACE) Wrapper Guide

ACE is best used as semantic retrieval: it finds likely files and code sections from intent, behavior, and architecture descriptions. It should not be treated as final evidence. Always verify important conclusions by reading files and using exact search for identifiers or call sites.

## Query Examples

### Conceptual Queries
```bash
# Understanding architecture
timeout 60s ace "How does the authentication flow work?" -w /path/to/project/root
timeout 60s ace "What is the request lifecycle in this application?" -w /path/to/project/root
timeout 60s ace "How are database transactions handled?" -w /path/to/project/root

# Finding implementations
timeout 60s ace "Where is the S3 upload logic located?" -w /path/to/project/root
timeout 60s ace "Find where uploaded files are validated, stored, and attached to messages" -w /path/to/project/root
timeout 60s ace "How are user permissions validated before tool execution?" -w /path/to/project/root

# Cross-language queries (Chinese to English code)
timeout 60s ace "用户登录流程在哪里实现" -w /path/to/project/root
timeout 60s ace "后台任务调度是怎么配置的" -w /path/to/project/root
```

### Workspace Management

```bash
# Search current directory (default)
timeout 60s ace "authentication logic"

# Search specific project root
timeout 60s ace "payment processing" -w /path/to/project/root

# Debug mode for troubleshooting
timeout 60s ace "config loading" -w /path/to/project/root --verbose
```

## Recommended Workflow

1. **Read guidance first**: check project instructions, README, or module docs when available.
2. **Semantic retrieval**: run `ace` for open-ended or intent-based questions.
3. **Inspect candidates**: read the top files/sections returned by ACE.
4. **Confirm precisely**: use `grep`/`rg` for exact identifiers, strings, events, tests, and call sites.
5. **Iterate**: if results are noisy, rewrite the query around behavior and data flow.

Example:

```bash
timeout 60s ace "user uploads an unsupported file and should see skipped-file feedback" -w /repo
rg -n "unsupported|skipped|upload|file" /repo
```

## Query Design

Good ACE queries usually include:

- User action: "drag files into chat", "click stop generation"
- Runtime boundary: "frontend to API", "CLI handler to core service"
- Expected effect: "abort active agent loop", "persist provider config"
- Known payload fields: `sessionId`, `files`, `workspace`, `requestId`

Avoid cramming unrelated questions into one query. Run separate queries for separate features.

```bash
# Good: one coherent workflow
timeout 60s ace "message composer sends text files workspace and requestId to backend and starts a processing job" -w /repo

# Better as separate queries, not one mixed request
timeout 60s ace "recover missed user data directory migration" -w /repo
timeout 60s ace "package publishing skips symlinks and dotfiles" -w /repo
timeout 60s ace "deferred capability discovery exposes matched tools in the next model request" -w /repo
```

## Reliability Boundaries

- ACE can return semantically nearby files for fictional or negative queries. Do not interpret output as proof that a feature exists.
- For "does this exist?" questions, require code evidence: a relevant implementation, test, config, or route.
- ACE may miss weaker subtopics in multi-intent queries.
- Exact identifiers and error strings are better found with literal search.

## Troubleshooting

### No Results Found

1. **Check authentication**
   ```bash
   auggie login
   ```

2. **Verify workspace path**
   Ensure the `-w` path points to the **project root directory**.
   ```bash
   ace "test query" -w /correct/project/root --verbose
   ```

3. **Refine query**
   - Use broader terms: "auth" instead of "OAuth2TokenValidator"
   - Use conceptual language: "how users log in" instead of "login function"
   - Try different phrasing: "user authentication" vs "login flow"

### Connection Errors

1. Verify internet connectivity
2. Check if Augment service is available
3. Re-authenticate: `auggie login`

### Empty or Unexpected Results

- The query may be too specific - try broader terms
- The codebase may not be indexed yet - wait and retry
- Use `--verbose` to see debug information
- The query may contain multiple unrelated topics - split it
- The returned files may be approximate matches - verify by reading code

## Best Practices

1. **Start broad, then narrow**
   - First: `ace "how does caching work"`
   - Then: `ace "Redis cache implementation"`

2. **Use natural language**
   - Good: "How are API errors handled?"
   - Less effective: "error handler function"

3. **Use hybrid retrieval**
   - **Prefer `ace`** for conceptual or intent-based searches.
   - Use **`grep-like`** tools for exact, literal keyword matching and confirmation.
   - Read files before making claims from search output.

4. **Priority of Tools and Performance**
   - **Performance**: Semantic search may take longer than literal search; ensure appropriate timeouts are set when calling from agents or scripts.

5. **Combine with other tools**
   - Use `ace` to discover relevant files
   - Use `Read` to examine specific implementations

## Exit Codes

| Code | Meaning |
| :--- | :--- |
| 0 | Success (results found or clean exit) |
| 1 | Error (path not found, auth failed, etc.) |

## References
- [Augment SDK Documentation](https://docs.augmentcode.com/context-services/sdk/overview#filesystem-context)
