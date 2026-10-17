#!/usr/bin/env python3
"""Require a higher plugin version for payload changes against an explicit Git base.

Read-only; includes staged, unstaged, and untracked candidate files. CI-only
workflow and .gitignore changes do not change the distributed guidance contract.
This checks version traceability, not live host behavior or release approval.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(*arguments: str) -> str:
    result = subprocess.run(["git", *arguments], cwd=ROOT, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", check=True)
    return result.stdout


def version(text: str) -> tuple[int, int, int]:
    manifest = json.loads(text)
    if not isinstance(manifest, dict):
        raise ValueError("plugin.json must be an object")
    value = manifest.get("version")
    if not isinstance(value, str) or not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", value):
        raise ValueError("plugin.json must contain a numeric major.minor.patch version")
    return tuple(int(part) for part in value.split("."))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True,
                        help="Explicit comparison commit/ref; all-zero only for a root commit")
    args = parser.parse_args(argv)
    try:
        current = version((ROOT / "plugin.json").read_text(encoding="utf-8"))
        # New refs have no before SHA, but may already have commit history.
        new_ref = len(args.base) in (40, 64) and set(args.base) == {"0"}
        if new_ref:
            history = git("rev-list", "--parents", "-n", "1", "HEAD").split()
            if len(history) > 1:
                raise ValueError("new ref with existing history requires an explicit --base commit/ref")
            base = None
        else:
            base = git("rev-parse", "--verify", "--end-of-options",
                       f"{args.base}^{{commit}}").strip()
        previous = None
        if base:
            changed = git("diff", "--name-only", "--no-renames", "-z", base, "--").split("\0")
            changed += git("ls-files", "--others", "--exclude-standard", "-z").split("\0")
            if git("ls-tree", "--name-only", base, "--", "plugin.json").strip():
                previous = version(git("show", f"{base}:plugin.json"))
        else:
            changed = git("ls-files", "--cached", "--others", "--exclude-standard", "-z").split("\0")
        payload = [name for name in changed
                   if name and name != ".gitignore" and not name.startswith(".github/")]
        if payload and previous is not None and current <= previous:
            raise ValueError("payload changed without a higher plugin.json version "
                             f"(base={'.'.join(map(str, previous))}, "
                             f"candidate={'.'.join(map(str, current))})")
        head = git("rev-parse", "--verify", "HEAD").strip()
        print(f"Release version check passed: version={'.'.join(map(str, current))}, "
              f"HEAD={head}, base={base or 'initial'}, payload_changes={len(payload)}")
        print("Candidate includes working-tree changes; live host validation is separate.")
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        detail = error.stderr.strip() if isinstance(error, subprocess.CalledProcessError) else str(error)
        print(f"Release version check failed: {detail}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
