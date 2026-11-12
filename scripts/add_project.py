#!/usr/bin/env python3
"""Interactively add a project to assets/projects.yaml."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required:  sudo apt install python3-yaml   (or pip install pyyaml)")

DEFAULT_FILE = Path(__file__).resolve().parent.parent / "assets" / "projects.yaml"
ONGOING_STATUSES = ("ongoing", "paused", "planned")


def slugify(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()


def ask(msg: str, default: str | None = None, required: bool = True) -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        try:
            raw = input(f"{msg}{suffix}: ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            sys.exit(1)
        if raw:
            return raw
        if default is not None:
            return default
        if not required:
            return ""
        print("  (required)")


def ask_date(msg: str, default: str | None = None, allow_blank: bool = False) -> date | None:
    while True:
        raw = ask(msg, default=default, required=not allow_blank)
        if not raw:
            return None
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("  Use YYYY-MM-DD")


def load(path: Path) -> dict:
    if not path.exists():
        return {"version": "2.0.0", "areas": []}
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    data.setdefault("version", "2.0.0")
    data.setdefault("areas", [])
    return data


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, default_flow_style=False,
                       allow_unicode=True, width=1000)


def pick_area(data: dict) -> dict:
    areas = data["areas"]
    if areas:
        print("\nExisting areas:")
        for i, a in enumerate(areas, 1):
            n = len(a.get("projects", []))
            print(f"  {i}) {a['label']:<26} ({a['id']}, {n} project{'s' if n != 1 else ''})")
        print("  n) + new area")
        raw = ask("Area")
        if raw.lower() not in ("n", "new"):
            try:
                return areas[int(raw) - 1]
            except (ValueError, IndexError):
                print("  invalid number, creating a new area instead.")

    label = ask("\nNew area label (e.g. Robotics)")
    default_id = slugify(label)
    while True:
        area_id = slugify(ask("Area id (slug)", default=default_id))
        if not any(a["id"] == area_id for a in areas):
            break
        print(f"  area '{area_id}' already exists")
    area = {"id": area_id, "label": label, "projects": []}
    areas.append(area)
    return area


def pick_status(has_end_date: bool) -> str:
    if has_end_date:
        return "completed"
    print("\nStatus:")
    for i, s in enumerate(ONGOING_STATUSES, 1):
        print(f"  {i}) {s}")
    while True:
        raw = ask("Status", default="ongoing")
        if raw in ONGOING_STATUSES:
            return raw
        try:
            return ONGOING_STATUSES[int(raw) - 1]
        except (ValueError, IndexError):
            print("  pick 1-3 or type a status")


def ask_repositories() -> list[dict]:
    repos = []
    print("\nRepositories  (leave name blank to finish)")
    while True:
        name = ask("  name", required=False)
        if not name:
            return repos
        url = ask("  url")
        repos.append({"name": name, "url": url})


def build_project(area: dict) -> dict:
    existing = {p.get("id") for p in area["projects"]}
    title = ask("\nProject title")
    default_id = slugify(title)
    while True:
        pid = slugify(ask("Project id (slug)", default=default_id))
        if pid not in existing:
            break
        print(f"  '{pid}' already used in this area")
    start = ask_date("Start date (YYYY-MM-DD)", default=date.today().isoformat())
    end = ask_date("End date (YYYY-MM-DD, blank = ongoing)", allow_blank=True)
    status = pick_status(end is not None)
    project = {"id": pid, "title": title, "start": start, "end": end, "status": status}
    repos = ask_repositories()
    if repos:
        project["repositories"] = repos
    return project


def list_projects(data: dict) -> None:
    for area in data["areas"]:
        print(f"\n{area['label']}  ({area['id']})")
        for p in area.get("projects", []):
            end = p.get("end") or "—"
            print(f"  • {p['title']:<24} [{p['status']:<9}] {p['start']} → {end}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Add a project to projects.yaml")
    ap.add_argument("-f", "--file", type=Path, default=DEFAULT_FILE)
    ap.add_argument("-l", "--list", action="store_true", help="list projects and exit")
    args = ap.parse_args()

    data = load(args.file)
    if args.list:
        list_projects(data)
        return

    area = pick_area(data)
    project = build_project(area)
    area["projects"].append(project)
    save(args.file, data)
    print(f"\n✔ added '{project['title']}' → {area['label']}  ({args.file})")


if __name__ == "__main__":
    main()