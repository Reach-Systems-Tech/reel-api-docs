#!/bin/bash
#
# File: extract_docs.sh
# Title: Documentation Archive Extraction
# Company: Reach Systems Ltd
# Author: Zeke Critchlow
# Date: June 5th, 2025
# Description: Extracts documentation archives with shared assets handling
#

set -e  # Exit on any error

# Function to show usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --version VERSION       Version being deployed"
    echo "  --download-url URL      URL to download archive from"
    echo "  --uses-shared-assets    Whether archive uses shared assets structure"
    echo "  --help                  Show this help message"
    exit 1
}

# Function to verify shared asset links in HTML files
verify_asset_links() {
    local version="$1"
    local file_path="docs/$version/index.html"
    
    if [ -f "$file_path" ]; then
        echo "Verifying shared asset links for version $version..."
        
        # Check CSS link
        if grep -q 'href="../styles.css"' "$file_path"; then
            echo "  CORRECT: Version file links to shared CSS"
        else
            echo "  ERROR: Version file missing shared CSS link"
            return 1
        fi
        
        # Check JS link  
        if grep -q 'src="../scripts.js"' "$file_path"; then
            echo "  CORRECT: Version file links to shared JS"
        else
            echo "  ERROR: Version file missing shared JS link"
            return 1
        fi
        
        return 0
    else
        echo "  ERROR: Version file not found at $file_path"
        return 1
    fi
}

# Function to verify template type
verify_template_type() {
    local version="$1"
    local file_path="docs/$version/index.html"
    
    if [ -f "$file_path" ]; then
        if grep -q "redoc-container" "$file_path"; then
            echo "  CORRECT: Version index.html contains Redoc template"
            return 0
        else
            echo "  ERROR: Version index.html does not contain Redoc template"
            echo "  First 200 chars of version index.html:"
            head -c 200 "$file_path"
            
            if grep -q "Auto-redirecting" "$file_path"; then
                echo "  This is the WRONG template (landing page)!"
                echo "  EXTRACTION FAILED: Landing page template copied to version location"
                return 1
            else
                echo "  Unknown template type"
                return 1
            fi
        fi
    else
        echo "  ERROR: Version-specific index.html missing at $file_path"
        return 1
    fi
}

# Function to extract shared assets
extract_shared_assets() {
    local extract_dir="$1"
    
    echo "=== SHARED ASSETS EXTRACTION ==="
    
    local shared_assets=("styles.css" "scripts.js" "icon.png" ".nojekyll")
    
    for asset in "${shared_assets[@]}"; do
        if [ -f "$extract_dir/$asset" ]; then
            echo "Updating shared asset: $asset"
            cp "$extract_dir/$asset" "docs/$asset"
            echo "  Updated docs/$asset ($(wc -c < docs/$asset) bytes)"
        else
            echo "  Shared asset $asset not found in archive"
        fi
    done
}

# Function to extract version-specific files
extract_version_files() {
    local extract_dir="$1"
    local version="$2"
    
    echo "=== VERSION-SPECIFIC FILES EXTRACTION ==="
    
    # Handle version-specific content
    if [ -d "$extract_dir/$version" ]; then
        echo "Found version-specific directory in archive: $extract_dir/$version"
        
        # Create version directory
        mkdir -p "docs/$version"
        
        # Copy ONLY the version-specific files
        echo "Copying version-specific files from $extract_dir/$version/ to docs/$version/"
        cp -r "$extract_dir/$version"/* "docs/$version/"
        
        echo "Skipping archive versions.json to preserve repo state"
        echo "CORRECT extraction: Version-specific files to docs/$version/"
        
    elif [ -d "$extract_dir/docs/api/auto_docs" ]; then
        echo "Found nested docs/api/auto_docs structure - extracting correctly..."
        
        local nested_path="$extract_dir/docs/api/auto_docs"
        
        # Handle shared assets from nested structure
        extract_shared_assets "$nested_path"
        
        # Create version directory and copy version-specific files
        mkdir -p "docs/$version"
        if [ -d "$nested_path/$version" ]; then
            echo "Moving version-specific files from $nested_path/$version/ to docs/$version/"
            cp -r "$nested_path/$version"/* "docs/$version/"
        else
            echo "ERROR: Version directory not found in nested structure!"
            find "$extract_dir" -type d -name "$version"
            return 1
        fi
        
    else
        echo "ERROR: Unrecognized archive structure!"
        echo "Expected either:"
        echo "  - Flat structure with $version/ directory and shared assets"
        echo "  - Nested docs/api/auto_docs/ structure"
        echo ""
        echo "Found structure:"
        find "$extract_dir" -type d
        return 1
    fi
    
    # Copy tools if they exist
    if [ -d "$extract_dir/_tools" ]; then
        cp -r "$extract_dir/_tools" "docs/$version/"
        echo "Copied _tools directory"
    fi
}

# Function to verify extraction results
verify_extraction() {
    local version="$1"
    
    echo "=== POST-EXTRACTION VERIFICATION ==="
    echo "Final extracted structure:"
    find "docs/$version" -type f | head -15
    echo "Total files extracted: $(find "docs/$version" -type f | wc -l)"
    
    # Verify shared assets
    echo ""
    echo "Shared assets verification:"
    local shared_assets=("styles.css" "scripts.js" "icon.png" ".nojekyll")
    
    for asset in "${shared_assets[@]}"; do
        if [ -f "docs/$asset" ]; then
            echo "  docs/$asset exists ($(wc -c < docs/$asset) bytes)"
        else
            echo "  docs/$asset missing!"
        fi
    done
    
    # Verify key files exist in correct locations
    if [ -f "docs/$version/index.html" ]; then
        echo ""
        echo "Version-specific index.html found at docs/$version/index.html"
        
        # Check file size
        local file_size=$(wc -c < "docs/$version/index.html")
        echo "File size: $file_size bytes"
        
        # Verify template type
        verify_template_type "$version" || return 1
        
        # Verify shared asset links
        verify_asset_links "$version" || return 1
        
    else
        echo "ERROR: Version-specific index.html missing at docs/$version/index.html"
        echo "Available files:"
        ls -la "docs/$version/"
        return 1
    fi
    
    # Check for documentation updater tool
    if [ -f "docs/$version/_tools/doc_updater.py" ]; then
        echo "Documentation updater tool found"
    else
        echo "Documentation updater tool missing!"
        echo "Available files in version directory:"
        find "docs/$version" -name "*.py" || echo "No Python files found"
    fi
}

# Main function
main() {
    local version=""
    local download_url=""
    local uses_shared_assets="false"
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --version)
                version="$2"
                shift 2
                ;;
            --download-url)
                download_url="$2"
                shift 2
                ;;
            --uses-shared-assets)
                uses_shared_assets="true"
                shift
                ;;
            --help)
                usage
                ;;
            *)
                echo "Unknown option: $1"
                usage
                ;;
        esac
    done
    
    # Validate required arguments
    if [ -z "$version" ] || [ -z "$download_url" ]; then
        echo "Error: --version and --download-url are required"
        usage
    fi
    
    echo "Downloading docs for version: $version"
    echo "Uses shared assets: $uses_shared_assets"
    echo "Download URL: $download_url"
    
    # Download the archive
    curl -L "$download_url" -o docs.tar.gz
    
    # Debug: Show what we downloaded
    echo "Archive contents preview:"
    tar -tzf docs.tar.gz | head -20
    
    # Extract to temp directory first to see structure
    mkdir -p temp_extract
    tar -xzf docs.tar.gz -C temp_extract
    
    echo "Extracted archive structure:"
    find temp_extract -type f | head -20
    
    # Extract shared assets first
    extract_shared_assets "temp_extract"
    
    # Extract version-specific files
    extract_version_files "temp_extract" "$version"
    
    # Clean up temp directory
    rm -rf temp_extract
    
    # Verify extraction results
    verify_extraction "$version"
    
    echo "Documentation extraction completed successfully"
}

# Run main function if script is executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi