#!/usr/bin/env python3
"""
Version management script for b62.

This script helps manage semantic versioning automatically.
"""

import re
import sys
from pathlib import Path


def get_current_version() -> str:
    """Get the current version from __init__.py."""
    init_file = Path("src/b62/__init__.py")
    content = init_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Could not find __version__ in __init__.py")
    return match.group(1)


def update_version(version: str) -> None:
    """Update the version in __init__.py."""
    init_file = Path("src/b62/__init__.py")
    content = init_file.read_text()
    new_content = re.sub(
        r'__version__\s*=\s*["\'][^"\']+["\']', f'__version__ = "{version}"', content
    )
    init_file.write_text(new_content)
    print(f"Updated version to {version}")


def parse_version(version: str) -> tuple[int, int, int, str | None]:
    """Parse semantic version string."""
    # Handle pre-release versions like 1.0.0-alpha.1
    match = re.match(r"(\d+)\.(\d+)\.(\d+)(?:-(.+))?", version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")

    major, minor, patch = map(int, match.groups()[:3])
    prerelease = match.group(4) if match.group(4) else None
    return major, minor, patch, prerelease


def bump_version(version: str, bump_type: str) -> str:
    """Bump version according to semantic versioning."""
    major, minor, patch, prerelease = parse_version(version)

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
        prerelease = None
    elif bump_type == "minor":
        minor += 1
        patch = 0
        prerelease = None
    elif bump_type == "patch":
        patch += 1
        prerelease = None
    elif bump_type == "prerelease":
        if prerelease:
            # Extract number from prerelease (e.g., "alpha.1" -> 1)
            prerelease_match = re.search(r"(\d+)$", prerelease)
            if prerelease_match:
                prerelease_num = int(prerelease_match.group(1)) + 1
                prerelease = re.sub(r"\d+$", str(prerelease_num), prerelease)
            else:
                prerelease += ".1"
        else:
            prerelease = "alpha.1"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")

    new_version = f"{major}.{minor}.{patch}"
    if prerelease:
        new_version += f"-{prerelease}"

    return new_version


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/version.py <command> [args]")
        print("Commands:")
        print("  current                    - Show current version")
        print("  current --version-only     - Show current version (version only)")
        print(
            "  bump <type>                - Bump version (major|minor|patch|prerelease)"
        )
        print("  set <version>              - Set specific version")
        print("  tag                        - Create git tag for current version")
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "current":
            version = get_current_version()
            if len(sys.argv) > 2 and sys.argv[2] == "--version-only":
                print(version)
            else:
                print(f"Current version: {version}")

        elif command == "bump":
            if len(sys.argv) < 3:
                print("Error: bump type required (major|minor|patch|prerelease)")
                sys.exit(1)
            bump_type = sys.argv[2]
            current_version = get_current_version()
            new_version = bump_version(current_version, bump_type)
            update_version(new_version)
            print(f"Bumped version from {current_version} to {new_version}")

        elif command == "set":
            if len(sys.argv) < 3:
                print("Error: version required")
                sys.exit(1)
            version = sys.argv[2]
            # Validate version format
            parse_version(version)
            update_version(version)
            print(f"Set version to {version}")

        elif command == "tag":
            version = get_current_version()
            import os
            import subprocess

            tag_name = f"v{version}"

            # Check if tag already exists
            result = subprocess.run(
                ["git", "tag", "-l", tag_name], capture_output=True, text=True
            )
            if result.stdout.strip():
                print(f"Tag {tag_name} already exists")
                sys.exit(1)

            # Create and push tag
            subprocess.run(
                ["git", "add", "src/python_redis_factory/__init__.py"], check=True
            )
            subprocess.run(
                ["git", "commit", "-m", f"chore: Bump version to {version}"], check=True
            )
            subprocess.run(
                ["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"], check=True
            )

            # In CI environment, we might not be able to push to main branch
            # but we can still create the tag locally for the release
            if os.environ.get("CI"):
                print(f"Created tag {tag_name} in CI environment")
                # Try to push tag, but don't fail if we can't push to main
                try:
                    subprocess.run(["git", "push", "origin", tag_name], check=True)
                    print(f"Pushed tag {tag_name} to remote")
                except subprocess.CalledProcessError:
                    print(f"Warning: Could not push tag {tag_name} to remote")
            else:
                # Local development - push both commit and tag
                subprocess.run(["git", "push", "origin", "main"], check=True)
                subprocess.run(["git", "push", "origin", tag_name], check=True)
                print(f"Created and pushed tag {tag_name}")

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
