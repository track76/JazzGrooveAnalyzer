# Developer Toolchain

This document describes the development tools used by the Jazz Groove Analyzer.

---

## Starting a New Development Session

Before starting a new development session, export the current project context:

```bash
python tools/export_chat_context.py
```

The command generates:

- `JGA_CONTEXT.zip`
- `JGA_BOOTSTRAP.md`

Use both files to initialize a new development session.

---

## Workflow

1. Complete the current work.
2. Ensure all tests pass.
3. Commit and push the repository.
4. Run:

```bash
python tools/export_chat_context.py
```

5. Start a new development session.
6. Attach:

- `JGA_CONTEXT.zip`
- `JGA_BOOTSTRAP.md`

---

## Notes

The repository is the single source of truth.

`JGA_BOOTSTRAP.md` and `JGA_CONTEXT.zip` are generated artifacts used to initialize a new development session.

If any information contained in these artifacts conflicts with the repository, the repository always prevails.
