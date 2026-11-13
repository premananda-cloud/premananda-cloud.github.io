# `assets/projects.yaml`: Schema Reference

| | |
|---|---|
| Location | `assets/projects.yaml` |
| Schema version | `2.0.0` |
| Encoding | UTF-8 |
| Indentation | 2 spaces, no tabs |

Top-level keys: `version`, `updated`, `areas`.

```yaml
version: "2.0.0"
updated: 2026-11-12
areas:
  - id: ai-ml
    label: AI / ML
    projects: [...]
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `version` | string | yes | Schema version. Always quoted. |
| `updated` | date | no | `YYYY-MM-DD`. Bumped by the CLI. |
| `areas` | list[Area] | yes | Ordered; order is the display order. |

## Naming conventions

One rule for every `id` (areas and projects):

- lowercase ASCII letters, digits and hyphens only (`production-apps`, `bert-spst`)
- no leading or trailing hyphen, no underscores
- unique across the whole file (not just within an area), since ids are used
  for anchors and cross-links

Other conventions:

- `title` / `label`: display text, written as the project is branded
  (`CampusWari`, `BERT SPST`).
- Repository `name`: short label shown on the page.
- Repository `url`: plain HTTPS repo URL, **no `.git` suffix**, so it is a
  clickable link as-is.
- YAML keys are `snake_case` or single lowercase words; never abbreviate or
  misspell (`title`, not `tittle`).

## Area

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | slug | yes | See naming conventions. |
| `label` | string | yes | Display name. |
| `projects` | list[Project] | yes | Ordered; may be empty. |

## Project

```yaml
- id: agere
  title: AGERE
  start: 2026-08-25
  end: null
  status: ongoing
  repositories:
    - name: AGERE
      url: https://github.com/premananda-cloud/AGERE
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | slug | yes | See naming conventions. |
| `title` | string | yes | Display name. |
| `start` | date | yes | `YYYY-MM-DD`. |
| `end` | date or null | yes | Date if finished, otherwise `null`. Never a word like `ongoing`. |
| `status` | enum | yes | `completed`, `ongoing`, `paused`, `planned`. |
| `repositories` | list[Repository] | no | Omit the key if there are none. |

### `status` and `end`

| `status` | Meaning | `end` |
|----------|---------|-------|
| `completed` | Finished | a date |
| `ongoing` | Actively worked on | `null` |
| `paused` | Started, on hold | `null` |
| `planned` | Not started | `null` |

For `planned` projects, `start` is the intended start date.

### Repository

| Field | Type | Required |
|-------|------|----------|
| `name` | string | yes |
| `url` | string (URL) | yes |

Always a list of `{name, url}` objects. No bare URLs, no one-key maps.

## Dates

- ISO `YYYY-MM-DD`, unquoted: PyYAML parses them to `datetime.date`.
- "No end date" is bare `null`. Not `"ongoing"`, `"present"`, `~` or `""`.

## Loading in Python

```python
import yaml
from pathlib import Path

data = yaml.safe_load(Path("assets/projects.yaml").read_text())
for area in data["areas"]:
    for p in area["projects"]:
        print(p["title"], p["status"], p["start"], p["end"])
```

## Common mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| `tittle:` | Key silently ignored | `title` |
| `end: ongoing` | `str` mixed with `date` | `end: null` + `status: ongoing` |
| `version: 2.0` unquoted | Parsed as float | `version: "2.0.0"` |
| `repositories: https://...` | Not a list | `- name: ...` / `url: ...` |
| `- AGERE: url` | `repo["url"]` fails | Use `{name, url}` |
| Underscore ids (`ai_ml`) | Breaks slug rule | `ai-ml` |
| Tabs | Parse error | 2 spaces |

## Changelog

- **2.0.0**: `areas` list with `id`/`label`; per-project `id`; `end` is
  `date | null` with a separate `status`; repositories are `{name, url}`
  lists; `tittle` renamed `title`. The old flat `projects:` shape is no longer
  supported.
