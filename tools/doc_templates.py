# tools/doc_templates.py
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

SEMVER_RE = re.compile(r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?")

def version_sort_key(v: str) -> tuple[int, int, int]:
    m = SEMVER_RE.match(v)
    if not m:
        return (0, 0, 0)
    a, b, c = m.groups()
    return (int(a or 0), int(b or 0), int(c or 0))


@dataclass(frozen=True)
class DocConfig:
    title: str = "ReelAPI v1"


def render_version_page_html(version: str, cfg: DocConfig) -> str:
    title = cfg.title
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


def render_landing_page_html(cfg: DocConfig) -> str:
    title = cfg.title
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} Documentation</title>
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
            <div class="reach-header-title">{title} Documentation</div>
        </div>
    </div>

    <div class="landing-container">
        <h1>{title} Documentation</h1>
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


def load_versions_json(docs_dir: Path) -> List[str]:
    vf = docs_dir / "versions.json"
    if not vf.exists():
        return []
    return json.loads(vf.read_text())


def ensure_landing_page(docs_dir: Path, cfg: DocConfig) -> None:
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "index.html").write_text(render_landing_page_html(cfg), encoding="utf-8")


def write_version_page(docs_dir: Path, version: str, cfg: DocConfig) -> None:
    version_dir = docs_dir / version
    version_dir.mkdir(parents=True, exist_ok=True)
    (version_dir / "index.html").write_text(render_version_page_html(version, cfg), encoding="utf-8")