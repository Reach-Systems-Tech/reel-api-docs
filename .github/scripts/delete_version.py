#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description="Delete a published docs version")
    p.add_argument("--docs-dir", default="docs")
    p.add_argument("--version", required=True)
    p.add_argument(
        "--keep-if-missing",
        action="store_true",
        help="Do not error if version directory doesn't exist",
    )
    args = p.parse_args()

    docs_dir = Path(args.docs_dir)
    version = args.version.strip()
    version_dir = docs_dir / version
    versions_file = docs_dir / "versions.json"

    # 1) Delete docs/<version> directory
    if version_dir.exists():
        if not version_dir.is_dir():
            raise SystemExit(f"Refusing to delete non-directory path: {version_dir}")
        shutil.rmtree(version_dir)
        print(f"Deleted directory: {version_dir}")
    else:
        msg = f"Version directory not found: {version_dir}"
        if args.keep_if_missing:
            print(msg)
        else:
            raise SystemExit(msg)

    # 2) Update versions.json (remove version)
    if versions_file.exists():
        try:
            versions = json.loads(versions_file.read_text(encoding="utf-8"))
            if not isinstance(versions, list):
                raise ValueError("versions.json is not a JSON list")
        except Exception as e:
            raise SystemExit(f"Failed to read versions.json: {e}")

        new_versions = [v for v in versions if str(v) != version]
        if new_versions != versions:
            versions_file.write_text(
                json.dumps(new_versions, indent=2) + "\n", encoding="utf-8"
            )
            print(f"Removed {version} from versions.json")
        else:
            print(f"{version} not present in versions.json (no change)")
    else:
        print("versions.json not found (no change)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
