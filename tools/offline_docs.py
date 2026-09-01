#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

from tools.doc_templates import DocConfig, render_offline_version_page_html


def build_offline_docs(
    docs_dir: Path,
    version: str,
    cfg: DocConfig,
) -> Path:
    version_dir = docs_dir / version
    openapi_file = version_dir / "openapi.json"
    scalar_file = docs_dir / "vendor" / "scalar" / "api-reference.js"

    if not openapi_file.exists():
        raise SystemExit(f"Missing OpenAPI spec: {openapi_file}")

    if not scalar_file.exists():
        raise SystemExit(f"Missing vendored Scalar bundle: {scalar_file}")

    openapi_spec = json.loads(openapi_file.read_text(encoding="utf-8"))

    downloads_dir = docs_dir / "downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)

    archive_name = f"reelapi-docs-{version}-offline"
    output_zip = downloads_dir / f"{archive_name}.zip"

    with tempfile.TemporaryDirectory() as tmp:
        package_dir = Path(tmp) / f"ReelAPI-{version}"
        scalar_dir = package_dir / "scalar"

        scalar_dir.mkdir(parents=True)

        (package_dir / "index.html").write_text(
            render_offline_version_page_html(version, openapi_spec, cfg),
            encoding="utf-8",
        )

        shutil.copy2(openapi_file, package_dir / "openapi.json")
        shutil.copy2(scalar_file, scalar_dir / "api-reference.js")

        for asset in ("icon.png", "favicon.ico"):
            source = docs_dir / asset
            if source.exists():
                shutil.copy2(source, package_dir / asset)

        archive_base = downloads_dir / archive_name

        shutil.make_archive(
            str(archive_base),
            "zip",
            root_dir=package_dir.parent,
            base_dir=package_dir.name,
        )

    print(f"Created: {output_zip}")
    return output_zip


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate offline ReelAPI documentation archive"
    )
    parser.add_argument("--docs-dir", default="docs")
    parser.add_argument("--version", required=True)
    parser.add_argument("--title", default="ReelAPI v1")
    args = parser.parse_args()

    build_offline_docs(
        Path(args.docs_dir),
        args.version.strip(),
        DocConfig(title=args.title),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())