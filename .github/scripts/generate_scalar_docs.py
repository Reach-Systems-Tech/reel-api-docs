#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow importing tools/doc_templates.py
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tools.doc_templates import DocConfig, ensure_landing_page, write_version_page  # noqa


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--docs-dir", default="docs")
    p.add_argument("--version", required=True)
    p.add_argument("--title", default="ReelAPI v1")
    args = p.parse_args()

    docs_dir = Path(args.docs_dir)
    scripts_path = docs_dir / "scripts.js"
    if not scripts_path.exists():
        raise SystemExit(f"Missing required file: {scripts_path}")

    scripts = scripts_path.read_text(encoding="utf-8")
    required = [
        "function loadVersions",
        "function setupLandingPage",
        "function switchVersion",
    ]
    missing = [r for r in required if r not in scripts]
    if missing:
        raise SystemExit(f"docs/scripts.js missing required functions: {missing}")

    # Generate the new version page
    cfg = DocConfig(title=args.title)
    write_version_page(docs_dir, args.version, cfg)

    # Ensure landing page always matches current template
    ensure_landing_page(docs_dir, cfg)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())