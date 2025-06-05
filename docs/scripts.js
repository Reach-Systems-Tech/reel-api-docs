// Shared JavaScript for Reach Systems API Documentation

// Common version switching function
function switchVersion(version, currentVersion) {
    if (version === currentVersion) return;
    
    // Get the current path and extract the base documentation path
    const currentPath = window.location.pathname;
    
    // Smart path detection for different deployment scenarios
    let basePath;
    
    // Check if we're in a GitHub Pages environment
    const isGitHubPages = window.location.hostname.includes('github.io');
    
    if (isGitHubPages) {
        // GitHub Pages: /repo-name/version/ format
        const pathParts = currentPath.split('/').filter(p => p);
        
        // Find the current version directory - FIXED REGEX ESCAPING
        const currentVersionIndex = pathParts.findIndex(part => 
            /^(test\d*|\d+(\.\d+)*)$/.test(part) || part === 'latest'
        );
        
        if (currentVersionIndex >= 0) {
            // Keep everything up to (but not including) the current version directory
            const basePathParts = pathParts.slice(0, currentVersionIndex);
            basePath = '/' + basePathParts.join('/');
            if (basePath !== '/') basePath += '/';
        } else {
            // Fallback: assume we're at repo root
            basePath = '/' + (pathParts[0] || '') + '/';
        }
    } else {
        // Local or custom domain deployment
        if (currentPath.includes('/docs/')) {
            // Extract base path up to /docs/
            basePath = currentPath.substring(0, currentPath.indexOf('/docs/') + 6);
        } else {
            // Simple case: find and replace current version
            const pathParts = currentPath.split('/').filter(p => p);
            const currentVersionIndex = pathParts.findIndex(part => 
                /^(test\d*|\d+(\.\d+)*)$/.test(part)
            );
            
            if (currentVersionIndex >= 0) {
                const basePathParts = pathParts.slice(0, currentVersionIndex);
                basePath = '/' + basePathParts.join('/');
                if (basePath !== '/') basePath += '/';
            } else {
                basePath = '/';
            }
        }
    }
    
    // Construct the new path
    const newPath = basePath + version + '/';
    
    console.log('Switching from', currentPath, 'to', newPath);
    window.location.href = newPath;
}

// Smart version loading with multiple fallback paths
function loadVersions(currentVersion, populateCallback) {
    // Calculate relative paths based on current location
    const currentPath = window.location.pathname;
    const pathDepth = currentPath.split('/').filter(p => p).length;
    
    // Build relative path to root
    let relativePath = '';
    if (pathDepth > 1) {
        // We're in a subdirectory, go up one level
        relativePath = '../';
    }
    
    const versionsPaths = [
        './versions.json',                    // Same directory (for root pages)
        relativePath + 'versions.json',       // Relative to root
        '../versions.json',                   // Parent directory (for version subdirs)
        '../../versions.json',               // Two levels up
        '/versions.json',                    // Absolute root
        // GitHub Pages specific paths
        window.location.pathname.split('/').slice(0, -2).join('/') + '/versions.json'
    ];
    
    function tryLoadVersions(pathIndex = 0) {
        if (pathIndex >= versionsPaths.length) {
            console.error('Could not load versions.json from any path');
            console.log('Tried paths:', versionsPaths);
            return;
        }
        
        const path = versionsPaths[pathIndex];
        console.log(`Trying to load versions from: ${path}`);
        
        fetch(path)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response.json();
            })
            .then(versions => {
                console.log('Successfully loaded versions:', versions);
                if (populateCallback) {
                    populateCallback(versions, currentVersion);
                }
            })
            .catch(error => {
                console.log(`Failed to load from ${path}:`, error.message);
                // Try next path
                tryLoadVersions(pathIndex + 1);
            });
    }
    
    // Start trying paths
    tryLoadVersions();
}

// Populate version dropdown for Redoc pages
function populateVersionDropdown(versions, currentVersion) {
    const select = document.getElementById('version-select');
    if (!select) return;
    
    // Clear existing options
    select.innerHTML = '';
    
    // Add all versions
    versions.forEach(v => {
        const option = document.createElement('option');
        option.value = v;
        option.textContent = v;
        if (v === currentVersion) {
            option.selected = true;
        }
        select.appendChild(option);
    });
}

// Auto-redirect functionality for landing page
function setupAutoRedirect(targetVersion, delay = 3000) {
    setTimeout(() => {
        window.location.href = targetVersion + '/';
    }, delay);
}
