#!/usr/bin/env python3
"""Install the ChatGPT/Codex transfer pack for local AI hosts.

Python 3.11+, standard library only. Intended entry after:
  git clone https://github.com/yjj3019/ChatGPT.git && cd ChatGPT

Preferred Codex usage is still opening this clone as a workspace so AGENTS.md
loads. Skill-style hosts get a copy under <skills-root>/chatgpt-transfer/.
ChatGPT Project Instructions (web) cannot be fully automated; use --print-chatgpt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import ntpath
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath, PureWindowsPath

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK_NAME = "chatgpt-transfer"
REQUIRED_FILES = ("CHATGPT.md", "AGENTS.md", "README.md", "README.en.md")
REQUIRED_DIRS = ("docs", "prompts", "scripts")
OPTIONAL_DIRS = ("tests",)
MANIFEST_FILE = ".chatgpt-transfer-manifest.json"
GENERATED_FILES = ("SKILL.md", "INSTALL_NOTE.md")
# Use Windows rules on every host; Python 3.11/3.12 need the pathlib fallback.
WINDOWS_IS_RESERVED = getattr(ntpath, "isreserved", lambda name: PureWindowsPath(name).is_reserved())

# (label, home marker dir, skills/packs root relative to home)
HOSTS: list[tuple[str, str, str]] = [
    ("Claude Code", ".claude", ".claude/skills"),
    ("Codex CLI", ".codex", ".agents/skills"),
    ("Grok", ".grok", ".grok/skills"),
    ("AGENTS.md compatible", ".agents", ".agents/skills"),
    ("Cursor", ".cursor", ".cursor/skills"),
]
FALLBACK_SKILLS_DIR = ".agents/skills"

COPY_IGNORE = shutil.ignore_patterns(
    "__pycache__",
    "*.pyc",
    ".pytest_cache",
    ".git",
    ".github",
)


def _utf8_console() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


def detect_targets(home: Path | None = None) -> list[tuple[str, Path]]:
    """Return (label, skills-or-packs-root) for detected AI hosts and env overrides."""
    home = home or Path.home()
    found: list[tuple[str, Path]] = []
    seen: set[Path] = set()

    for label, marker, skills_dir in HOSTS:
        if not (home / marker).is_dir():
            continue
        target = (home / skills_dir).absolute()
        if target not in seen:
            seen.add(target)
            found.append((label, target))

    for env_name in ("AI_PACK_DIR", "AI_SKILLS_DIR", "CURSOR_PACK_DIR", "CURSOR_SKILLS_DIR"):
        raw = os.environ.get(env_name)
        if not raw:
            continue
        target = Path(raw).expanduser().absolute()
        if target not in seen:
            seen.add(target)
            found.append((f"${env_name}", target))

    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        target = (Path(codex_home).expanduser() / "skills").absolute()
        if target not in seen:
            seen.add(target)
            found.append(("$CODEX_HOME/skills", target))

    return found


def pack_source_paths(with_tests: bool) -> list[tuple[str, Path]]:
    """Relative name → absolute source path for items to copy."""
    items: list[tuple[str, Path]] = []
    for name in REQUIRED_FILES:
        path = REPO_ROOT / name
        if not path.is_file():
            raise SystemExit(f"Missing required pack file: {name}")
        items.append((name, path))
    for name in REQUIRED_DIRS:
        path = REPO_ROOT / name
        if not path.is_dir():
            raise SystemExit(f"Missing required pack directory: {name}")
        items.append((name, path))
    if with_tests:
        for name in OPTIONAL_DIRS:
            path = REPO_ROOT / name
            if path.is_dir():
                items.append((name, path))
    readme_ko = REPO_ROOT / "README.ko.md"
    if readme_ko.is_file():
        items.append(("README.ko.md", readme_ko))
    return items


def skill_hint() -> str:
    """Render a narrow skill entry, not a second always-loaded runtime."""
    description = (
        "Apply the chatgpt-transfer guidance when the user requests this pack "
        "for a task or a setup review. Not for unrelated coding or writing."
    )
    return (
        "---\nname: " + json.dumps(PACK_NAME) + "\ndescription: "
        + json.dumps(description) + "\n---\n"
        + """# ChatGPT / Codex Transfer Pack

Use when this pack is requested, including explicit skill invocation. Do not
replace the user's chosen workflow or apply the pack to unrelated tasks.

Read [AGENTS.md](AGENTS.md) relative to this SKILL.md directory as the minimal
entry, then read only the task-relevant guides it selects, relative to this pack.
Do not preload CHATGPT.md as a second entry or load every guide. Host and existing
workspace instructions still take precedence; invoking a skill does not make
this directory the host's primary folder or auto-load its AGENTS.md.

For a requested ChatGPT Project setup, use [README.en.md](README.en.md) or
[README.md](README.md). Files being installed does not prove discovery, activation,
or access in a live client. Keep the current model and granted permissions.
"""
    )


def validate_skill_metadata(content: str) -> None:
    """Check this generator's two JSON-quoted YAML scalars, not arbitrary YAML."""
    lines = content.splitlines()
    if len(lines) < 5 or lines[0] != "---" or lines[3] != "---":
        raise ValueError("invalid SKILL.md frontmatter")
    metadata = {}
    for line in lines[1:3]:
        key, separator, value = line.partition(": ")
        if not separator or key not in {"name", "description"} or key in metadata:
            raise ValueError("invalid SKILL.md metadata keys")
        try:
            metadata[key] = json.loads(value)
        except ValueError as exc:
            raise ValueError("invalid SKILL.md metadata scalar") from exc
    description = metadata.get("description")
    if (metadata.get("name") != PACK_NAME or not isinstance(description, str)
            or not description.strip() or len(description) > 1024
            or any(ord(char) < 32 for char in description)):
        raise ValueError("invalid SKILL.md name or description")


def bootstrap_note() -> str:
    """Short note at pack root pointing Codex users at AGENTS.md / clone workflow."""
    note = """# Installed pack bootstrap

This directory is a copy of the ChatGPT/Codex transfer pack for skill-style hosts.

Distribution baseline: preserve recipient models, permissions, and settings.
See docs/distribution-standard.md for model-inheriting role examples; installation
does not activate role files, named presets, or memory features.

**Preferred Codex setup:** clone https://github.com/yjj3019/ChatGPT.git and open that
repository as the workspace so `AGENTS.md` loads at the workspace root.

**This copy:** invoke the skill; its instructions explicitly read the adjacent
`AGENTS.md`. Installing files alone does not prove host discovery or activation.
Keep Operational Integrity and Context Budget unchanged across models.

**ChatGPT Project:** paste `CHATGPT.md` into Project Instructions; attach needed `docs/` files.
Run `python scripts/install_pack.py --print-chatgpt` from a clone for exact steps.

**Verify files:** `python scripts/install_pack.py --check --dest <skills-root>`
from the clone, using the original installation destination. This checks files,
not live host loading; use the README smoke check to verify actual application.
"""
    return note


def _safe_path(path: Path) -> None:
    """Reject links/reparse points before resolving or reading their targets."""
    for part in (path, *path.parents):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"Symlink or junction is not supported: {part}")


def _hash(path: Path) -> str:
    _safe_path(path)
    if not path.is_file():
        raise ValueError(f"Not a regular file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_files(with_tests: bool) -> dict[str, str]:
    files = {}
    _safe_path(REPO_ROOT)
    for relative, source in pack_source_paths(with_tests):
        _safe_path(source)
        if source.is_file():
            files[relative] = _hash(source)
            continue
        for directory, dirs, names in os.walk(source, followlinks=False):
            ignored = COPY_IGNORE(directory, dirs + names)
            dirs[:] = [name for name in dirs if name not in ignored]
            for name in dirs + [name for name in names if name not in ignored]:
                _safe_path(Path(directory) / name)
            for name in names:
                if name not in ignored:
                    path = Path(directory) / name
                    files[path.relative_to(REPO_ROOT).as_posix()] = _hash(path)
    return files


def _read_manifest(pack: Path) -> dict:
    _safe_path(pack / MANIFEST_FILE)
    manifest = json.loads((pack / MANIFEST_FILE).read_text(encoding="utf-8"))
    if (not isinstance(manifest, dict) or type(manifest.get("version")) is not int or manifest["version"] != 1
            or type(manifest.get("with_tests")) is not bool
            or not isinstance(manifest.get("files"), dict) or not manifest["files"]):
        raise ValueError("invalid manifest format")
    for name, checksum in manifest["files"].items():
        if (not isinstance(name, str) or not name or "\\" in name or ":" in name
                or "\x00" in name or PurePosixPath(name).is_absolute()
                or any(part in {"", ".", ".."} or part.endswith((".", " "))
                       or WINDOWS_IS_RESERVED(part) for part in name.split("/"))
                or any(ord(c) < 32 for c in name)
                or name == MANIFEST_FILE or not isinstance(checksum, str)
                or len(checksum) != 64 or any(c not in "0123456789abcdef" for c in checksum)):
            raise ValueError("invalid manifest path or checksum")
    required = (*REQUIRED_FILES, *GENERATED_FILES, "scripts/install_pack.py",
                "scripts/sync_runtime.py", "scripts/validate_framework.py")
    if not set(required).issubset(manifest["files"]):
        raise ValueError("manifest is missing required files")
    if manifest["with_tests"] and "tests/Scorecard.md" not in manifest["files"]:
        raise ValueError("manifest is missing tests")
    return manifest


def verify_install(dest_pack: Path) -> list[str]:
    """Verify shipped content; unrelated user files are preserved and ignored."""
    try:
        _safe_path(dest_pack)
        manifest = _read_manifest(dest_pack)
    except (OSError, ValueError) as exc:
        return [f"invalid or missing integrity manifest: {exc}"]
    problems = []
    for name in REQUIRED_DIRS:
        try:
            _safe_path(dest_pack / name)
            if not (dest_pack / name).is_dir():
                problems.append(f"missing directory: {name}")
        except (OSError, ValueError) as exc:
            problems.append(str(exc))
    for name, checksum in manifest["files"].items():
        try:
            if _hash(dest_pack / name) != checksum:
                problems.append(f"modified file: {name}")
        except (OSError, ValueError) as exc:
            problems.append(f"cannot verify {name}: {exc}")
    try:
        _safe_path(dest_pack / "SKILL.md")
        validate_skill_metadata((dest_pack / "SKILL.md").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        problems.append(str(exc))
    return problems


def install_pack(skills_root: Path, *, with_tests: bool = False,
                 dry_run: bool = False, force: bool = False) -> Path:
    """Skip identical installs; refuse differences unless explicitly forced.

    Stage and verify before replacement. A failed publish restores the old pack.
    This is not a lock against hostile concurrent filesystem modifications.
    """
    skills_root = skills_root.expanduser().absolute()
    dest = skills_root / PACK_NAME
    try:
        _safe_path(dest)
        _safe_path(REPO_ROOT)
        source_root, target = REPO_ROOT.resolve(), dest.resolve()
        if target.is_relative_to(source_root) or source_root.is_relative_to(target):
            raise ValueError("Source and destination overlap")
        if skills_root.exists() and not skills_root.is_dir():
            raise ValueError(f"Destination is not a directory: {skills_root}")
        if dest.exists() and not dest.is_dir():
            raise ValueError(f"Pack destination is not a directory: {dest}")
        files = _source_files(with_tests)
        generated = {"SKILL.md": skill_hint(), "INSTALL_NOTE.md": bootstrap_note()}
        validate_skill_metadata(generated["SKILL.md"])
        files.update({name: hashlib.sha256(text.encode("utf-8")).hexdigest()
                      for name, text in generated.items()})
        expected = {"version": 1, "with_tests": with_tests, "files": files}
        if dest.exists():
            if not force and not verify_install(dest) and _read_manifest(dest) == expected:
                print(f"Unchanged (preserved): {dest}")
                return dest
            if not force:
                raise ValueError(f"Refusing to overwrite existing pack at {dest}. "
                                 "Back up user files, then pass --force to replace.")
            print(f"WARNING: --force replaces ALL contents, including user files: {dest}",
                  file=sys.stderr)
        if dry_run:
            return dest
        skills_root.mkdir(parents=True, exist_ok=True)
        work = Path(tempfile.mkdtemp(prefix=".chatgpt-transfer-", dir=skills_root))
        stage, backup = work / "new", work / "old"
        published = False
        try:
            stage.mkdir()
            for relative, source in pack_source_paths(with_tests):
                if source.is_dir():
                    shutil.copytree(source, stage / relative, ignore=COPY_IGNORE)
                else:
                    shutil.copy2(source, stage / relative)
            for name, text in generated.items():
                (stage / name).write_text(text, encoding="utf-8", newline="\n")
            copied = {}
            for path in stage.rglob("*"):
                _safe_path(path)
                if path.is_file():
                    copied[path.relative_to(stage).as_posix()] = _hash(path)
            if copied != files:
                raise ValueError("Staged content differs from source snapshot; retry installation")
            (stage / MANIFEST_FILE).write_text(json.dumps(expected, sort_keys=True, indent=2)
                                               + "\n", encoding="utf-8")
            problems = verify_install(stage)
            if problems:
                raise ValueError("Staged verification failed: " + "; ".join(problems))
            _safe_path(dest)
            if dest.exists():
                dest.rename(backup)
            try:
                stage.rename(dest)
                published = True
            except OSError:
                if backup.exists():
                    backup.rename(dest)
                raise
        finally:
            if published or not backup.exists():
                shutil.rmtree(work)
            else:
                print(f"Recovery required; original pack retained at {backup}", file=sys.stderr)
        return dest
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc


def run_validate(tree: Path) -> int:
    """Run validate_framework.py from an installed or source tree. Return exit code."""
    script = tree / "scripts" / "validate_framework.py"
    if not script.is_file():
        print(f"validate script missing: {script}", file=sys.stderr)
        return 1
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(script)],
        cwd=str(tree),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


def print_chatgpt_steps() -> None:
    entry = REPO_ROOT / "CHATGPT.md"
    print("ChatGPT Project Instructions (web) — paste steps")
    print("=" * 60)
    print("1. Open ChatGPT → create or open a Project.")
    print("2. Open Project Instructions / Custom instructions for the project.")
    print("3. Paste the full contents of CHATGPT.md (path below).")
    print(f"   File: {entry}")
    print("4. Attach needed docs/ files as project knowledge (coding, domain, etc.).")
    print("   Do not attach the full transfer guide or all-in-one unless requested.")
    print("5. Keep Context Budget: Core + 1–2 mapped guides (or one task + one domain section).")
    print("6. Model choice (advisory): see docs/chatgpt-codex-model-routing.md")
    print("   Use the current model by default; preserve integrity and context limits.")
    print()
    print("Exact file to paste:")
    print(f"  {entry}")
    if entry.is_file():
        size = entry.stat().st_size
        print(f"  ({size} bytes UTF-8 on disk)")


def destination_root(value: str | None) -> Path:
    if value:
        return Path(value).expanduser()
    for env_name in ("AI_PACK_DIR", "AI_SKILLS_DIR", "CURSOR_PACK_DIR", "CURSOR_SKILLS_DIR"):
        raw = os.environ.get(env_name)
        if raw:
            return Path(raw).expanduser()
    if raw := os.environ.get("CODEX_HOME"):
        return Path(raw).expanduser() / "skills"
    raise SystemExit(
        "Set --dest, AI_PACK_DIR / AI_SKILLS_DIR / CURSOR_* / CODEX_HOME, or use --auto."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python scripts/install_pack.py --auto\n"
            "  python scripts/install_pack.py --dest ~/.agents/skills\n"
            "  python scripts/install_pack.py --print-chatgpt\n"
            "  python scripts/install_pack.py --check --dest ~/.agents/skills\n"
        ),
    )
    parser.add_argument("--dest", help="Parent skills/packs directory (pack lands in <dest>/chatgpt-transfer/)")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Detect AI hosts and install into each skills directory "
        f"(fallback: ~/{FALLBACK_SKILLS_DIR})",
    )
    parser.add_argument(
        "--list-targets",
        action="store_true",
        help="Print detected install targets without installing",
    )
    parser.add_argument(
        "--print-chatgpt",
        action="store_true",
        help="Print exact steps to paste CHATGPT.md into ChatGPT Project Instructions",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify installed pack files and run validate_framework.py",
    )
    parser.add_argument(
        "--with-tests",
        action="store_true",
        help="Also copy tests/ into the installed pack",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show destinations without copying files",
    )
    parser.add_argument("--force", action="store_true",
                        help="Replace ALL existing pack contents, including user files; back up first")
    args = parser.parse_args(argv)
    _utf8_console()

    if args.print_chatgpt:
        print_chatgpt_steps()
        return 0

    if args.list_targets:
        targets = detect_targets()
        if targets:
            for label, path in targets:
                print(f"{label}: {path}")
        else:
            print(f"No AI host detected — default: {Path.home() / FALLBACK_SKILLS_DIR}")
        return 0

    if args.check:
        roots: list[Path] = []
        if args.dest:
            roots.append(Path(args.dest).expanduser() / PACK_NAME)
        elif args.auto:
            targets = detect_targets()
            if not targets:
                targets = [("fallback", Path.home() / FALLBACK_SKILLS_DIR)]
            roots.extend(root / PACK_NAME for _, root in targets)
        else:
            # Prefer checking an explicit dest; otherwise validate the source tree.
            try:
                roots.append(destination_root(None) / PACK_NAME)
            except SystemExit:
                roots.append(REPO_ROOT)

        failed = False
        for pack in roots:
            print(f"Checking: {pack}")
            # Only a checkout is a source tree. Installed scripts run with their
            # own pack as REPO_ROOT, even after install metadata is removed.
            source_checkout = pack == REPO_ROOT and (pack / ".git").exists()
            problems = [] if source_checkout else verify_install(pack)
            if source_checkout:
                for name in REQUIRED_FILES:
                    if not (pack / name).is_file():
                        problems.append(f"missing file: {name}")
                for name in REQUIRED_DIRS:
                    if not (pack / name).is_dir():
                        problems.append(f"missing directory: {name}")
            if problems:
                failed = True
                for problem in problems:
                    print(f"  FAIL: {problem}")
                continue
            print("  files OK")
            # Full validate needs tests/; installs without --with-tests only get file checks.
            if (pack / "tests" / "Scorecard.md").is_file():
                code = run_validate(pack)
                if code != 0:
                    failed = True
                else:
                    print("  validate OK")
            else:
                print("  validate skipped (tests/ not installed; reinstall with --with-tests)")
        return 1 if failed else 0

    if args.auto:
        targets = detect_targets()
        if not targets:
            fallback = Path.home() / FALLBACK_SKILLS_DIR
            print(f"No AI host detected — installing to shared location: {fallback}")
            targets = [("AGENTS.md compatible (fallback)", fallback)]
        summaries: list[str] = []
        for label, root in targets:
            dest = install_pack(root, with_tests=args.with_tests, dry_run=args.dry_run, force=args.force)
            action = "Would install" if args.dry_run else "Installed"
            line = f"{action}: {dest}  ({label})"
            print(line)
            summaries.append(line)
            if not args.dry_run:
                problems = verify_install(dest)
                if problems:
                    print("  problems: " + "; ".join(problems), file=sys.stderr)
                    return 1
        print()
        print("Summary:")
        for line in summaries:
            print(f"  {line}")
        print()
        print("Next steps:")
        print("  Codex  → open the git clone as workspace (loads AGENTS.md), or use the installed pack.")
        print("  ChatGPT → python scripts/install_pack.py --print-chatgpt")
        print("  Verify  → python scripts/install_pack.py --check --auto")
        return 0

    # Explicit --dest or env-based single install
    root = destination_root(args.dest)
    dest = install_pack(root, with_tests=args.with_tests, dry_run=args.dry_run, force=args.force)
    action = "Would install" if args.dry_run else "Installed"
    print(f"{action}: {dest}")
    if not args.dry_run:
        problems = verify_install(dest)
        if problems:
            print("Installation incomplete:", file=sys.stderr)
            for problem in problems:
                print(f"  - {problem}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        raise SystemExit(0)
