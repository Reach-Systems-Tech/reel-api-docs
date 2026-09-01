#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from tools.doc_templates import (
    DocConfig,
    load_versions_json,
    version_sort_key,
    write_version_page,
)
from tools.offline_docs import build_offline_docs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Backfill offline documentation for published API versions"
    )
    parser.add_argument("--docs-dir", default="docs")
    parser.add_argument("--title", default="ReelAPI v1")
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    cfg = DocConfig(title=args.title)

    versions = load_versions_json(docs_dir)

    if not versions:
        raise SystemExit(f"No published versions found in {docs_dir / 'versions.json'}")

    generated = 0
    skipped = 0

    for version in sorted(versions, key=version_sort_key):
        version_dir = docs_dir / version
        openapi_file = version_dir / "openapi.json"

        if not openapi_file.exists():
            print(f"SKIP  {version:>8s}  - missing openapi.json")
            skipped += 1
            continue

        print(f"BUILD {version:>8s}")

        # Regenerate online page so it contains the offline download link.
        write_version_page(docs_dir, version, cfg)

        # Generate the version-specific offline archive.
        build_offline_docs(docs_dir, version, cfg)

        generated += 1

    print()
    print("Backfill complete:")
    print(f"  {generated} versions generated")
    if skipped:
        print(f"  {skipped} versions skipped")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())