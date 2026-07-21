# AGENTS.md — textcharts

Instructions for AI agents working in this repository. Keep changes minimal,
prefer the project's existing patterns, and use `uv` for all Python.

## TODO tracker (authoritative: project-isolated `todo-db` database)

As of **2026-07-21** this project's tracker was migrated from the legacy YAML
system to a **project-isolated `todo-db` database**. The database is the record.

- **Database:** `.todo-db/standalone.sqlite` — local SQLite, git-ignored, never
  committed. Identity is pinned to `project_id=textcharts`; a mismatched
  project id or repository is rejected by the tool.
- **The ONLY supported write/read path is the adapter** `_project/scripts/todo`.
  Do not invoke `todo-db` directly against the database, and never hand-write
  tracker state into repo files or use raw SQL. Examples:

  ```bash
  _project/scripts/todo list          # all items
  _project/scripts/todo ready         # actionable work units
  _project/scripts/todo stats         # summary
  _project/scripts/todo show <id>     # one item
  _project/scripts/todo claim <id>    # lifecycle mutations …
  _project/scripts/todo <cmd> --help  # full CLI contract; exit 2 means fix the cause
  ```

- **Rebuild** the database from the retained YAML at any time (zero-loss,
  deterministic): `_project/scripts/rebuild_todo_db.sh`. It refuses to
  overwrite an existing database.

- The unpublished `todo-db` tool is resolved from a sibling checkout
  (`TODO_DB_HOME`, default `/Users/joe/Developer/todo-db`). There is no PyPI
  resolution.

## Skills: `todo` vs `todo-db`

- **`todo`** — idea → specification authoring ONLY (ideate / brainstorm /
  refine / write a spec). It performs no tracker reads or writes.
- **`todo-db`** — every tracker query and lifecycle mutation (create, list,
  ready, claim, start, done, defer, promote, dismiss, complete, block, lint,
  verify, batch, …). Tracker state lives in the database and flows through the
  `_project/scripts/todo` adapter.

Skill text is distributed by skill-sync (mirror mode) from
`~/.skill-sync/skills`; the copies under `.claude/`, `.codex/`, `.gemini/` are
generated mirrors — never edit them as a source of truth.

## Legacy YAML corpus (read-only rollback)

`_project/TODO/`, `_project/DONE/`, `todo.config.yaml`, `_project/TODO_SCHEMA.yaml`
and `_project/TODO_ENTRY_TEMPLATE.yaml` are the **pre-migration snapshot**,
retained verbatim for provenance and rollback. **Do not** hand-edit them as live
tracker state and do not delete them — legacy removal is a separate, explicitly
approved step. Every field the `todo-db` schema does not model (tags,
estimated_effort, owners, impact, files_affected, success_metrics,
context_sections, open_questions, sections, last_updated, moved_from) is
retained verbatim inside each imported item's `description` (see
`_project/scripts/todo_migrate_transform.py`), so the migration is lossless.

## Isolation

One physical database per project. Never point this project's tooling at another
project's database, replica, identity, or credentials, and never point a drill
or test at a protected planning/production database.
