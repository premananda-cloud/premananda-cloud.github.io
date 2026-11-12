# Projects Portfolio: Docs

Documents the project data model and the tooling that maintains it.

| File | Purpose |
|------|---------|
| [`yaml-structure.md`](./yaml-structure.md) | Schema reference for `assets/projects.yaml` |
| [`cli.md`](./cli.md) | Reference for `scripts/add_project.py` |

## How it fits together

- `assets/projects.yaml` is the single source of truth, grouped by area.
- `scripts/add_project.py` appends projects to it safely (no duplicate ids,
  consistent `status`/`end`).
- `index.html`, `index.css` and `main.py` render the portfolio from the YAML.

## Quick start

```bash
./scripts/add_project.py --list   # show everything, no writes
./scripts/add_project.py          # add a project interactively
```
