#!/usr/bin/env python3
"""Upsert the GitHub issue labels declared in ``.github/labels.toml``.

This replaces the abandoned ``labels`` PyPI CLI, which dies with
``TypeError: Label.__init__() got an unexpected keyword argument 'archived_at'``
because it unpacks every field of the labels API response into a fixed signature.

Only create and update happen here: remote labels missing from the manifest are left
alone on purpose, since deleting a label in use would erase triage history.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any


def gh(*args: str) -> Any:
    """Run a gh CLI command and return its JSON output."""
    process = subprocess.run(("gh", *args), capture_output=True, text=True)
    if process.returncode != 0:
        raise SystemExit(f"gh {' '.join(args)} failed: {process.stderr.strip()}")
    return json.loads(process.stdout)


def normalize(color: str) -> str:
    return color.removeprefix("#").lower()


def load_declared(manifest: Path) -> dict[str, dict[str, str]]:
    declared: dict[str, dict[str, str]] = {}
    for key, label in tomllib.loads(manifest.read_text(encoding="utf-8")).items():
        name = label.get("name") or key
        declared[name] = {"color": normalize(label["color"]), "description": label.get("description") or ""}
    return declared


def load_remote() -> dict[str, dict[str, str]]:
    rows = gh("label", "list", "--limit", "1000", "--json", "name,color,description")
    return {row["name"]: {"color": normalize(row["color"]), "description": row["description"] or ""} for row in rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path(".github/labels.toml"))
    parser.add_argument("--dry-run", action="store_true", help="print the planned changes without touching GitHub")
    args = parser.parse_args()

    declared = load_declared(args.manifest)
    remote = load_remote()

    changes = 0
    for name, want in sorted(declared.items()):
        have = remote.get(name)
        if have == want:
            continue
        action = "create" if have is None else "edit"
        changes += 1
        print(f"{action} {name}")
        if not args.dry_run:
            gh("label", action, name, "--color", want["color"], "--description", want["description"])

    extra = sorted(set(remote) - set(declared))
    if extra:
        print(f"kept {len(extra)} remote label(s) absent from the manifest: {', '.join(extra)}")
    print(f"{'would apply' if args.dry_run else 'applied'} {changes} change(s) to {len(declared)} declared label(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
