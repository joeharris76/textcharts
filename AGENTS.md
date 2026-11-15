# AGENTS.md — textcharts

Instructions for AI agents working in this repository. Keep changes minimal
and follow the project's existing patterns.

## TODO tracker (authoritative: project-isolated `todo-db` database)

The tracker is a **project-isolated `todo-db` database**; it is the record. It
runs the `todo-db` 0.3.2 wheel vendored in `_project/scripts/vendor/`, driven
through the `_project/scripts/todo` adapter. There is no sibling `todo-db`
checkout and no PyPI resolution.

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

- **Rebuild:** `_project/scripts/rebuild_todo_db.sh` rebuilds the database from
  the retained YAML, but it does not work today. It runs `uv run --project
  "$TODO_DB_HOME"` and `TODO_DB_HOME` defaults to `/Users/joe/Developer/todo-db`,
  which does not exist. It also refuses to overwrite an existing database. Do
  not tell the user a rebuild is available until the script is pointed at the
  vendored wheel.
- The global `todo` skill drives a different tracker (tractable) and does not
  apply in this repository. Use the adapter above.

The skill copies under `.claude/`, `.codex/`, `.gemini/` are skill-sync mirrors
of the catalog pinned in `skill-sync.yaml`. Edit the catalog (the
`skill-sync-skills` repository), never the mirrors.

## Legacy YAML corpus (read-only rollback)

`_project/TODO/`, `_project/DONE/`, `todo.config.yaml`, `_project/TODO_SCHEMA.yaml`
and `_project/TODO_ENTRY_TEMPLATE.yaml` are the **pre-migration snapshot**,
retained verbatim for provenance and rollback. **Do not** hand-edit them as live
tracker state and do not delete them — legacy removal is a separate, explicitly
approved step. Imported items keep every unmodelled legacy field verbatim in
`description` (see `_project/scripts/todo_migrate_transform.py`).

## Isolation

One physical database per project. Never point this project's tooling at another
project's database, replica, identity, or credentials, and never point a drill
or test at a protected planning/production database.
