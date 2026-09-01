# Reach Systems Reel API Documentation

This repository hosts the **public API documentation** for the Reach Systems Reel Control System API. The documentation is automatically generated and deployed from the private development repository.

## For API Clients

**[Access the Interactive API Documentation](https://reach-systems-tech.github.io/reel-api-docs/)**

The documentation provides:

- **Comprehensive Schema Documentation** - Detailed request/response examples
- **Version Management** - Access documentation for different API versions
- **Search Functionality** - Quickly find the endpoints you need
- **Offline Documentation** - Download a self-contained archive for a specific API version

### Getting Started

1. Visit the [documentation](https://reach-systems-tech.github.io/reel-api-docs/)
2. Select the API version you are integrating against
3. Review the authentication requirements
4. Explore the available endpoints using the interactive interface
5. Download the offline documentation archive if you need a local reference copy

### Offline Documentation

Offline documentation is published as a version-specific ZIP archive.

Each archive contains:

- A self-contained Scalar API reference that can be opened directly in a browser
- The OpenAPI specification for that API version
- Required Scalar and Reach Systems branding assets

No web server or internet connection is required after the archive has been extracted.

Each archive contains documentation for a single API version.

## For Reach Developers

This repository is part of the **automated documentation deployment pipeline** and serves as the public-facing documentation host.

### Repository Purpose

- **Documentation Host** - Serves API documentation via GitHub Pages
- **Version Management** - Maintains multiple versions of API documentation
- **Offline Archives** - Provides downloadable documentation snapshots for individual API versions
- **Shared Assets** - Uses centralized CSS, JavaScript, and branding assets
- **Vendored Dependencies** - Stores the Scalar browser bundle used to build offline documentation
- **Automated Deployment** - Receives updates from the private development repository

### Workflow

- **Source Repository** - [`Reach-Systems-Tech/p017_reach_web_portal_v2`](https://github.com/Reach-Systems-Tech/p017_reach_web_portal_v2) (private)
- **Documentation Generation** - Triggered by version tags in the private repo
- **Offline Package Generation** - Builds a version-specific ZIP from the published `openapi.json`

### File Structure

```text
docs/
├── styles.css                  # Shared CSS for online documentation
├── scripts.js                  # Shared JavaScript functionality
├── icon.png                    # Shared branding asset
├── favicon.ico                 # Shared favicon
├── .nojekyll                   # Disables Jekyll processing
├── index.html                  # Landing page with version list
├── versions.json               # Master list of available versions
├── vendor/
│   └── scalar/
│       ├── VERSION             # Vendored Scalar version
│       └── api-reference.js    # Scalar standalone browser bundle
├── downloads/
│   └── reelapi-docs-{version}-offline.zip
└── {version}/
    ├── index.html              # Scalar documentation page
    └── openapi.json            # OpenAPI specification
```

### Generating an Offline Archive Locally

To generate an offline archive for an existing API version:

```bash
python3 -m tools.offline_docs \
  --docs-dir docs \
  --version 1.5.21
```

The generated archive will be written to:

docs/downloads/reelapi-docs-1.5.21-offline.zip