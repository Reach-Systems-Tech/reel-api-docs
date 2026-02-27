#!/usr/bin/env python3
"""
Migrate reel-api-docs from Redoc to Scalar.

Run from the root of your reel-api-docs checkout:
    python3 migrate_to_scalar.py

What it does:
  1. Reads docs/versions.json
  2. For each version with an openapi.json, writes a new Scalar index.html
  3. Writes the new dynamic landing page at docs/index.html
  4. Backs up old index.html files as index.html.redoc
  5. Cleans up old .backup files from the doc_updater era
  6. Renames old styles.css / scripts.js to .old

What it does NOT touch:
  - versions.json (already correct)
  - openapi.json files (untouched)
  - icon.png (still used)
"""

import json
import re
import shutil
import sys
from pathlib import Path

DOCS_DIR = Path("docs")
TITLE = "ReelAPI v1"


# ─── Templates ───────────────────────────────────────────────────────────────

def version_page_html(version: str, title: str) -> str:
    """Scalar version page — loads openapi.json via fetch, shared CSS/JS from parent."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {version}</title>
    <link rel="stylesheet" href="../styles.css">
    <link rel="icon" type="image/x-icon" href="../favicon.ico">
</head>
<body class="has-header">
    <div class="reach-header">
        <div class="reach-header-left">
            <img
                src="../icon.png"
                alt="Reach Systems"
                class="reach-header-logo"
                onerror="this.style.display='none'"
            >
            <div class="reach-header-title">{title} Documentation</div>
        </div>
        <select
            class="reach-version-select"
            id="version-select"
            aria-label="Select API version"
            onchange="switchVersion(this.value, '{version}')"
        >
            <option selected>{version}</option>
        </select>
    </div>

    <div id="app"></div>

    <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
    <script src="../scripts.js"></script>
    <script>
        loadVersions('{version}');

        fetch('./openapi.json')
            .then(function (r) {{
            if (!r.ok) throw new Error('Failed to load openapi.json: ' + r.status);
            return r.json();
            }})
            .then(function (spec) {{
            Scalar.createApiReference('#app', {{
                content: spec,
                agent: {{
                disabled: true
                }}
            }});
            }})
            .catch(function (err) {{
            document.getElementById('app').innerHTML =
                '<div style="padding:40px;text-align:center;color:#666;">' +
                '<h2>Failed to load API specification</h2>' +
                '<p>' + err.message + '</p></div>';
            }});
        </script>
</body>
</html>"""


LANDING_PAGE_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE} Documentation</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="icon" type="image/x-icon" href="./favicon.ico">
</head>
<body class="has-header landing-page">
    <div class="reach-header">
        <div class="reach-header-left">
            <img
                src="icon.png"
                alt="Reach Systems"
                class="reach-header-logo"
                onerror="this.style.display='none'"
            >
            <div class="reach-header-title">{TITLE} Documentation</div>
        </div>
    </div>

    <div class="landing-container">
        <h1>{TITLE} Documentation</h1>
        <p class="subtitle">Cable Reel Control System API Reference</p>

        <div class="auto-redirect" id="redirect-banner">
            Loading latest version...
        </div>

        <h2>Available Versions</h2>
        <ul class="version-list" id="version-list">
            <li class="loading">Loading versions...</li>
        </ul>
    </div>

    <script src="scripts.js"></script>
    <script>
        setupLandingPage();
    </script>
</body>
</html>"""


# ─── Migration logic ─────────────────────────────────────────────────────────

def version_sort_key(v: str) -> tuple:
    match = re.match(r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?", v)
    if match:
        return tuple(int(p) if p else 0 for p in match.groups())
    return (0, 0, 0)


def backup_file(path: Path, suffix: str) -> bool:
    """Back up a file if no backup with that suffix exists yet. Returns True if backed up."""
    backup_path = path.parent / (path.name + suffix)
    if path.exists() and not backup_path.exists():
        shutil.copy2(path, backup_path)
        return True
    return False


def main():
    if not DOCS_DIR.is_dir():
        print(f"Error: {DOCS_DIR} not found. Run this from your reel-api-docs root.")
        sys.exit(1)

    versions_file = DOCS_DIR / "versions.json"
    if not versions_file.exists():
        print(f"Error: {versions_file} not found.")
        sys.exit(1)

    versions = json.loads(versions_file.read_text())
    print(f"Found {len(versions)} versions in versions.json\n")

    # ── Regenerate each version ──────────────────────────────────────────
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

        # Back up old Redoc page
        backup_file(index_file, ".redoc")

        # Write new Scalar page
        html = version_page_html(version, TITLE)
        index_file.write_text(html)
        success += 1
        print(f"    OK  {version:>8s}")

    # ── Landing page ─────────────────────────────────────────────────────
    landing_file = DOCS_DIR / "index.html"
    backup_file(landing_file, ".redoc")
    landing_file.write_text(LANDING_PAGE_HTML)
    print(f"\n    OK  landing page")

    # ── Clean up old artifacts ───────────────────────────────────────────
    # Rename old shared CSS/JS (no longer needed — CSS is now in styles.css with new classes)
    # Actually, we're REPLACING styles.css and scripts.js, so just note they'll be overwritten
    # by the user copying the new versions.

    # Delete old .backup files from the doc_updater era
    backup_count = 0
    for backup_file_path in DOCS_DIR.rglob("*.backup"):
        backup_file_path.unlink()
        backup_count += 1

    # ── Summary ──────────────────────────────────────────────────────────
    print(f"\n{'─' * 50}")
    print(f"Migration complete:")
    print(f"  {success} versions regenerated with Scalar")
    if skipped:
        print(f"  {skipped} versions skipped (no openapi.json)")
    print(f"  1 landing page created (dynamic versions.json)")
    if backup_count:
        print(f"  {backup_count} old .backup files deleted")
    print(f"\nOld Redoc pages backed up as index.html.redoc")
    print(f"\nIMPORTANT: Also copy the new shared files into docs/:")
    print(f"  cp styles.css  ~/src/reel-api-docs/docs/styles.css")
    print(f"  cp scripts.js  ~/src/reel-api-docs/docs/scripts.js")
    print(f"\nTest locally:")
    print(f"  cd docs && python3 -m http.server 8000")
    print(f"  Open http://localhost:8000")


if __name__ == "__main__":
    main()