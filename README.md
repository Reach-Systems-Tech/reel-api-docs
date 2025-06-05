# Reach Systems Reel API Documentation

This repository hosts the **public API documentation** for the Reach Systems Reel Control System API. The documentation is automatically generated and deployed from the private development repository.

## For API Clients

**[Access the Interactive API Documentation](https://reach-systems-tech.github.io/reel-api-docs/)**

The documentation provides:

- **Comprehensive Schema Documentation** - Detailed request/response examples
- **Version Management** - Access documentation for different API versions
- **Search Functionality** - Quickly find the endpoints you need

### Getting Started

1. Visit the [documentation](https://reach-systems-tech.github.io/reel-api-docs/)
2. Review the authentication requirements
3. Explore the available endpoints using the interface
4. Integrate the API into your application

## For Reach Developers

This repository is part of the **automated documentation deployment pipeline** and serves as the public-facing documentation host.

### Repository Purpose

- **Documentation Host** - Serves API documentation via GitHub Pages
- **Version Management** - Maintains multiple versions of API documentation
- **Shared Assets** - Uses centralized CSS, JavaScript, and branding assets
- **Automated Deployment** - Receives updates from the private development repository

### Workflow Integration

- **Source Repository** - [`Reach-Systems-Tech/p017_reach_web_portal_v2`](https://github.com/Reach-Systems-Tech/p017_reach_web_portal_v2) (private)
- **Documentation Generation** - Triggered by version tags in the private repo
- **Deployment Process** - Automated via GitHub Actions workflows
- **Asset Management** - Shared CSS/JS assets for consistent styling across versions

### Key Components

- **GitHub Pages** - Hosts documentation at `https://reach-systems-tech.github.io/reel-api-docs/`
- **Workflow Scripts** - Located in `.github/scripts/` for maintainability
- **Shared Assets** - `docs/styles.css`, `docs/scripts.js`, `docs/icon.png`
- **Version Control** - `docs/versions.json` manages available documentation versions

### Development Workflow

1. **Private Repository** - API development and documentation generation
2. **Version Tagging** - Triggers documentation build in private repo
3. **Archive Creation** - Documentation packaged and uploaded as GitHub release
4. **Repository Dispatch** - Triggers deployment workflow in this repository
5. **Asset Extraction** - Shared assets and version-specific files extracted
6. **GitHub Pages** - Updated documentation deployed automatically

### Maintenance

- **Workflow Files** - Located in `.github/workflows/deploy-docs.yml`
- **Helper Scripts** - Modular scripts in `.github/scripts/` for maintainability
- **Asset Updates** - Shared assets updated with each deployment
- **Version Sync** - All documentation versions kept in sync automatically

### File Structure

```bash
docs/
├── styles.css          # Shared CSS for all versions
├── scripts.js          # Shared JavaScript functionality  
├── icon.png            # Shared branding assets
├── .nojekyll           # Disables Jekyll processing
├── index.html          # Landing page with version list
├── versions.json       # Master list of available versions
├── {version}/          # Version-specific documentation
│   ├── index.html      # Redoc documentation page
│   ├── openapi.json    # OpenAPI specification
│   └── versions.json   # Copy of master versions list
```
