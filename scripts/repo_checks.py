#!/usr/bin/env python3
"""Repository hygiene checks.

Two failures this catches that nothing else would, because both are silent:

  1. A malformed YAML file. GitHub issue forms, dbt schemas, and workflow
     files all fail quietly when their YAML is wrong -- the form simply
     stops rendering, the model stops being recognised.
  2. A relative markdown link pointing at a file that does not exist.
     In a public docs repository these rot with every rename.
  3. A ROADMAP progress line that disagrees with its own checkboxes. A
     hand-written summary above a checklist lags it, and this one already
     has -- twice in one day.

Runs with no dependencies beyond PyYAML. Usable locally:
    python3 scripts/repo_checks.py

SPDX-License-Identifier: CC-BY-4.0
"""

from __future__ import annotations

import pathlib
import re
import sys

import yaml

SKIP_DIRS = {".git", "node_modules", ".venv", "target", "__pycache__"}

# Matches [text](target) but not image embeds preceded by '!'.
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")

EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#")

ROADMAP = "ROADMAP.md"

# "## Phase 3 - The grid" with either a hyphen or an em dash.
PHASE = re.compile(r"^## Phase (\d+) [-\u2014]")
BOX = re.compile(r"^\s*- \[([ x])\]")
PROGRESS = re.compile(r"^Progress: \*\*(.+)\*\*$", re.MULTILINE)


def walk(root: pathlib.Path, pattern: str):
    for path in root.rglob(pattern):
        if SKIP_DIRS.isdisjoint(path.parts):
            yield path


def check_yaml(root: pathlib.Path) -> list[str]:
    problems: list[str] = []
    for pattern in ("*.yml", "*.yaml"):
        for path in walk(root, pattern):
            try:
                list(yaml.safe_load_all(path.read_text(encoding="utf-8")))
            except yaml.YAMLError as exc:
                problems.append(f"{path}: invalid YAML: {exc}")
            except UnicodeDecodeError as exc:
                problems.append(f"{path}: not valid UTF-8: {exc}")
    return problems


def check_links(root: pathlib.Path) -> list[str]:
    problems: list[str] = []
    for path in walk(root, "*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            problems.append(f"{path}: not valid UTF-8: {exc}")
            continue
        for match in LINK.finditer(text):
            target = match.group(1).split("#")[0].strip()
            if not target or target.startswith(EXTERNAL_PREFIXES):
                continue
            if target.startswith("/"):
                resolved = root / target.lstrip("/")
            else:
                resolved = path.parent / target
            if not resolved.exists():
                problems.append(f"{path}: broken link -> {target}")
    return problems


def phase_counts(text: str) -> dict[int, tuple[int, int]]:
    """Boxes and ticks per phase, in the order the headings appear."""
    counts: dict[int, list[int]] = {}
    current: int | None = None
    for line in text.splitlines():
        heading = PHASE.match(line)
        if heading:
            current = int(heading.group(1))
            counts.setdefault(current, [0, 0])
            continue
        box = BOX.match(line)
        if box and current is not None:
            counts[current][0] += 1
            counts[current][1] += box.group(1) == "x"
    return {number: (total, ticked) for number, (total, ticked) in counts.items()}


def expected_progress(counts: dict[int, tuple[int, int]]) -> str:
    """The sentence the checkboxes support.

    Completion is read as a prefix from Phase 0, because that is what the
    roadmap claims: a later phase with ticks while an earlier one is open does
    not make the earlier one done, and the sentence names the first open phase
    either way.
    """
    numbers = sorted(counts)
    done: list[int] = []
    for number in numbers:
        total, ticked = counts[number]
        if total and ticked == total:
            done.append(number)
        else:
            break

    remaining = [number for number in numbers if number not in done]
    if not remaining:
        return "All phases complete."

    following = remaining[0]
    total, ticked = counts[following]
    if not done:
        head = ""
    elif len(done) == 1:
        head = f"Phase {done[0]} complete. "
    elif len(done) == 2:
        head = f"Phases {done[0]} and {done[1]} complete. "
    else:
        head = f"Phases {done[0]} to {done[-1]} complete. "

    if ticked == 0:
        tail = f"Phase {following} next."
    else:
        tail = f"Phase {following} in progress, {ticked} of {total}."
    return f"{head}{tail}"


def check_progress(root: pathlib.Path) -> list[str]:
    """Fail when the progress line disagrees with the boxes beneath it."""
    path = root / ROADMAP
    if not path.is_file():
        return [f"{ROADMAP}: not found, so the progress line cannot be checked"]

    text = path.read_text(encoding="utf-8")
    counts = phase_counts(text)
    if not counts:
        return [f"{ROADMAP}: no phase headings found, so nothing was checked"]

    found = PROGRESS.search(text)
    if not found:
        return [f"{ROADMAP}: no line matching 'Progress: **...**'"]

    expected = expected_progress(counts)
    if found.group(1) != expected:
        return [
            f"{ROADMAP}: progress line disagrees with the checkboxes\n"
            f"      says:   {found.group(1)}\n"
            f"      should: {expected}"
        ]
    return []


def main() -> int:
    root = pathlib.Path(".").resolve()
    problems = check_yaml(root) + check_links(root) + check_progress(root)

    if problems:
        print(f"{len(problems)} problem(s) found:\n")
        for problem in problems:
            print(f"  {problem}")
        return 1

    print("YAML valid, internal links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
