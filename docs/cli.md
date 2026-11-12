# `scripts/add_project.py`: CLI Reference

Interactive tool for adding projects to
[`assets/projects.yaml`](../../assets/projects.yaml). Schema:
[`yaml-structure.md`](./yaml-structure.md).

## Requirements

- Python 3.10+
- PyYAML (`sudo apt install python3-yaml`, or `pip install pyyaml`)

The script resolves the YAML path relative to itself, so it runs from any
directory.

```bash
chmod +x scripts/add_project.py   # once
```

## Usage

```bash
./scripts/add_project.py                    # add a project
./scripts/add_project.py --list             # list, never writes
./scripts/add_project.py -f path/other.yaml # use another file
```

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--file` | `-f` | `assets/projects.yaml` | YAML file to read/write |
| `--list` | `-l` | off | Print all areas and projects, then exit |

## Interactive flow

1. **Area**: pick by number, or `n` for a new one (asks for label, then an id
   derived from it; re-prompts on collision).
2. **Title**: display name.
3. **Project id**: slug derived from the title, editable, must be unique.
4. **Start date**: `YYYY-MM-DD`, default today.
5. **End date**: `YYYY-MM-DD`, or blank for none.
   - Date given: status becomes `completed`.
   - Blank: choose `ongoing` (default), `paused` or `planned`.
6. **Repositories**: `name` / `url` pairs; blank name to finish.

### Example session

```
$ ./scripts/add_project.py

Existing areas:
  1) AI / ML                  (ai-ml, 2 projects)
  2) Cryptography             (cryptography, 3 projects)
  3) Production Applications  (production-apps, 1 project)
  4) Utilities                (utilities, 1 project)
  5) Econometrics             (econometrics, 1 project)
  n) + new area
Area: n

New area label: Robotics
Area id (slug) [robotics]:

Project title: SLAM sandbox
Project id (slug) [slam-sandbox]:
Start date (YYYY-MM-DD) [2026-11-12]:
End date (YYYY-MM-DD, blank = none):
Status [ongoing]:

Repositories (blank name to finish)
  name: slam-sandbox
  url: https://github.com/premananda-cloud/slam-sandbox
  name:
Added 'SLAM sandbox' to Robotics
```

### Example `--list`

```
AI / ML  (ai-ml)
  - BERT SPST     [completed] 2026-01-05 -> 2026-03-31
  - AGERE         [ongoing  ] 2026-08-25 -> -
```

## Guarantees

- Never writes a duplicate area or project `id`.
- Always writes `repositories` as `{name, url}` objects.
- Keeps `status` and `end` consistent (date means `completed`, no date means
  `ongoing` / `paused` / `planned`).
- Keeps key order (`sort_keys=False`).
- Aborts on `Ctrl-C` / `Ctrl-D` without touching the file.

> The file is re-serialized on every write, so **YAML comments are not
> preserved**. Keep notes in these docs, not in the YAML.

## Failure modes

| Situation | Behaviour |
|-----------|-----------|
| PyYAML missing | Prints install hint, exit 1 |
| Target file missing | Starts a new `{version, areas: []}` document |
| Invalid YAML | Exits without writing |
| File has no `areas` key | Refuses to run (old 1.x format) |
| Blank required input | Re-prompts |

## Ideas for later

- `--area <id>` for non-interactive adds
- `--json` to emit `projects.json` for the browser
- `edit` subcommand
- `--check` validation (duplicate ids, `.git` suffixes, status/end mismatch),
  usable as a pre-commit hook
- `docs/projects/schema.json` for editor validation

Update the flags table and [`README.md`](./README.md) when any of these land.
