#!/usr/bin/env python3
"""
Migrate reel-api-docs from Redoc to Scalar.

Run from the root of your reel-api-docs checkout:
    python3 migrate_to_scalar.py
"""

import shutil
import sys
from pathlib import Path

from tools.doc_templates import (
    DocConfig,
    ensure_landing_page,
    load_versions_json,
    version_sort_key,
    write_version_page,
)

DOCS_DIR = Path("docs")
TITLE = "ReelAPI v1"


def backup_file(path: Path, suffix: str) -> bool:
    """Back up a file if no backup with that suffix exists yet. Returns True if backed up."""
    backup_path = path.parent / (path.name + suffix)
    if path.exists() and not backup_path.exists():
        shutil.copy2(path, backup_path)
        return True
    return False


def main() -> None:
    if not DOCS_DIR.is_dir():
        print(f"Error: {DOCS_DIR} not found. Run this from your reel-api-docs root.")
        sys.exit(1)

    versions_file = DOCS_DIR / "versions.json"
    if not versions_file.exists():
        print(f"Error: {versions_file} not found.")
        sys.exit(1)

    versions = load_versions_json(DOCS_DIR)
    print(f"Found {len(versions)} versions in versions.json\n")

    cfg = DocConfig(title=TITLE)

    success = 0
    skipped = 0

    for version in sorted(versions, key=version_sort_key):
        version_dir = DOCS_DIR / version
        spec_file = version_dir / "openapi.json"
        index_file = version_dir / "index.html"

        if not spec_file.exists():
            print(f"  SKIP  {version:>8s}  — no openapi.json")
            skipped += 1
            continue

        # Back up existing page (Redoc or older Scalar)
        backup_file(index_file, ".redoc")

        # Write Scalar page using shared template
        write_version_page(DOCS_DIR, version, cfg)
        success += 1
        print(f"    OK  {version:>8s}")

    # Landing page (always ensure it matches current template)
    landing_file = DOCS_DIR / "index.html"
    backup_file(landing_file, ".redoc")
    ensure_landing_page(DOCS_DIR, cfg)
    print(f"\n    OK  landing page")

    # Delete old .backup files from the doc_updater era
    backup_count = 0
    for backup_file_path in DOCS_DIR.rglob("*.backup"):
        backup_file_path.unlink()
        backup_count += 1

    print(f"\n{'─' * 50}")
    print("Migration complete:")
    print(f"  {success} versions regenerated with Scalar")
    if skipped:
        print(f"  {skipped} versions skipped (no openapi.json)")
    print("  1 landing page created (dynamic versions.json)")
    if backup_count:
        print(f"  {backup_count} old .backup files deleted")

    print("\nTest locally:")
    print("  cd docs && python3 -m http.server 8000")
    print("  Open http://localhost:8000")


if __name__ == "__main__":
    main()