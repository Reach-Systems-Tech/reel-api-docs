#!/usr/bin/env python3
"""
File: version_manager.py
Title: Version Manager Utilities
Company: Reach Systems Ltd
Author: Zeke Critchlow
Date: June 5th, 2025
Description: Utilities for managing documentation versions in the GitHub worflow.
"""

import json
import re
import os
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


def version_key(version: str) -> Tuple[int, int, int, str]:
    """
    Convert version string to sortable tuple.
    Returns (major, minor, patch, original_string) for semantic versions,
    or (0, 0, 0, original_string) for non-semantic versions.
    """
    match = re.match(r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?", version)
    if match:
        parts = match.groups()
        return tuple(int(p) if p else 0 for p in parts) + (version,)
    return (0, 0, 0, version)


def load_versions(versions_file: Path) -> List[str]:
    """Load existing versions from versions.json file."""
    if versions_file.exists():
        try:
            with open(versions_file, "r") as f:
                versions = json.load(f)
                print(f"Loaded existing versions: {versions}")
                return versions
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading versions.json: {e}")
            return []
    else:
        print("No existing versions.json found")
        return []


def save_versions(versions_file: Path, versions: List[str]) -> None:
    """Save versions list to versions.json file."""
    # Ensure parent directory exists
    versions_file.parent.mkdir(parents=True, exist_ok=True)

    with open(versions_file, "w") as f:
        json.dump(versions, f, indent=2)
    print(f"Saved versions.json with: {versions}")


def add_version(versions: List[str], new_version: str) -> List[str]:
    """Add new version to list if not already present."""
    if new_version not in versions:
        versions.append(new_version)
        print(f"Added new version. Updated list: {versions}")
    else:
        print(f"Version {new_version} already exists in list")
    return versions


def sort_versions(versions: List[str]) -> List[str]:
    """Sort versions by semantic version (newest first)."""
    sorted_versions = sorted(versions, key=version_key, reverse=True)
    print(f"Sorted versions: {sorted_versions}")
    return sorted_versions


def get_latest_version(versions: List[str]) -> str:
    """Get the latest (first) version from sorted list."""
    if versions:
        latest = versions[0]
        print(f"Latest version: {latest}")
        return latest
    return "unknown"


def update_versions(docs_dir: Path, new_version: str) -> str:
    """
    Main function to update versions.json with new version.
    Returns the latest version after update.
    """
    versions_file = docs_dir / "versions.json"

    print(f"Adding version: {new_version}")

    # Load existing versions
    versions = load_versions(versions_file)

    # Add new version
    versions = add_version(versions, new_version)

    # Sort versions (newest first)
    versions = sort_versions(versions)

    # Save updated versions
    save_versions(versions_file, versions)

    # Return latest version
    return get_latest_version(versions)


def main():
    """Main entry point when run as script."""
    parser = argparse.ArgumentParser(
        description="Update versions.json with semantic sorting"
    )
    parser.add_argument("--docs-dir", default="docs", help="Documentation directory")
    parser.add_argument("--version", required=True, help="New version to add")
    parser.add_argument("--output-latest", help="File to write latest version to")

    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)

    # Update versions and get latest
    latest_version = update_versions(docs_dir, args.version)

    # Optionally write latest version to file
    if args.output_latest:
        with open(args.output_latest, "w") as f:
            f.write(latest_version)
        print(f"Latest version written to: {args.output_latest}")

    print(f"Version update completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
