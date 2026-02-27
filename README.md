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

### Workflow

- **Source Repository** - [`Reach-Systems-Tech/p017_reach_web_portal_v2`](https://github.com/Reach-Systems-Tech/p017_reach_web_portal_v2) (private)
- **Documentation Generation** - Triggered by version tags in the private repo

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
│   ├── index.html      # Scalar documentation page
│   ├── openapi.json    # OpenAPI specification
│   └── versions.json   # Copy of master versions list
```
