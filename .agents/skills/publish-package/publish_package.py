#!/usr/bin/env python
"""Publish the financial-stock-agent package."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from packaging.version import Version

INIT_FILE = Path("finance_agent/__init__.py")


def run_command(command: list[str]) -> None:
    """Run a shell command."""
    print(f"$ {' '.join(command)}")

    subprocess.run(
        command,
        check=True,
    )


def get_current_version() -> Version:
    """Return the current package version."""
    content = INIT_FILE.read_text(encoding="utf-8")

    match = re.search(
        r'__version__:\s*str\s*=\s*"([^"]+)"',
        content,
    )

    if match is None:
        raise ValueError(f"Unable to find __version__ in {INIT_FILE}")

    return Version(match.group(1))


def update_version(new_version: Version) -> None:
    """Update finance_agent/__init__.py."""
    content = INIT_FILE.read_text(encoding="utf-8")

    updated = re.sub(
        r'(__version__:\s*str\s*=\s*")[^"]+(")',
        rf"\g<1>{new_version}\2",
        content,
    )

    INIT_FILE.write_text(
        updated,
        encoding="utf-8",
    )


def ensure_clean_git_status() -> None:
    """Ensure git working tree is clean."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )

    if result.stdout.strip():
        raise RuntimeError("Git working tree is not clean.")


def main() -> None:
    """Entry point."""
    if len(sys.argv) != 2:
        print(
            "Usage: publish_package.py VERSION",
            file=sys.stderr,
        )
        sys.exit(1)

    target_version = Version(sys.argv[1])

    ensure_clean_git_status()

    current_version = get_current_version()

    if target_version <= current_version:
        raise ValueError(
            f"Target version {target_version} "
            f"must be greater than current version "
            f"{current_version}"
        )

    print(f"Current version : {current_version}")
    print(f"Target version  : {target_version}")

    update_version(target_version)

    try:
        run_command(["uv", "build"])
        run_command(["uv", "publish"])

        run_command(
            [
                "git",
                "add",
                "finance_agent/__init__.py",
            ]
        )

        run_command(
            [
                "git",
                "commit",
                "-m",
                f"Publish v{target_version}",
            ]
        )

        run_command(
            [
                "git",
                "tag",
                "-a",
                f"v{target_version}",
                "-m",
                f"Release v{target_version}",
            ]
        )

    except Exception:
        print(
            "\nPublishing failed.",
            file=sys.stderr,
        )
        print(
            "You may need to manually revert finance_agent/__init__.py",
            file=sys.stderr,
        )
        raise

    print("\nRelease Summary")
    print("================")
    print(f"Previous version : {current_version}")
    print(f"Published version: {target_version}")
    print(f"Git commit       : Publish v{target_version}")
    print(f"Git tag          : v{target_version}")
    print("Package published successfully.")


if __name__ == "__main__":
    main()
