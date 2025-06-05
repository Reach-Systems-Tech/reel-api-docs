#!/bin/bash
#
# File: verify_structure.sh
# Title: Documentation Structure Verification
# Company: Reach Systems Ltd
# Author: Zeke Critchlow
# Date: June 5th, 2025
# Description: Verifies documentation structure and shared assets integrity
#

set -e  # Exit on any error

# Function to show usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --docs-dir DIR     Documentation directory (default: docs)"
    echo "  --verbose          Show detailed output"
    echo "  --help             Show this help message"
    exit 1
}

# Function to check if a version directory name is valid
is_valid_version() {
    local version="$1"
    # Match semantic versions (1.2.3) or test versions (test1, test2, etc.)
    if echo "$version" | grep -E '^[0-9]+(\.[0-9]+)*$' >/dev/null || echo "$version" | grep '^test' >/dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to verify shared assets
verify_shared_assets() {
    local docs_dir="$1"
    local verbose="$2"
    
    echo "=== SHARED ASSETS VERIFICATION ==="
    
    local shared_assets=("styles.css" "scripts.js" "icon.png" ".nojekyll")
    local missing_assets=()
    
    for asset in "${shared_assets[@]}"; do
        if [ -f "$docs_dir/$asset" ]; then
            local size=$(wc -c < "$docs_dir/$asset")
            echo "$asset exists ($size bytes)"
            
            if [ "$verbose" = "true" ]; then
                # Additional checks for specific assets
                case "$asset" in
                    "styles.css")
                        if grep -q ".header-bar" "$docs_dir/$asset"; then
                            echo "  CSS contains required header styles"
                        else
                            echo "  WARNING: CSS missing header styles"
                        fi
                        ;;
                    "scripts.js")
                        if grep -q "switchVersion" "$docs_dir/$asset"; then
                            echo "  JS contains version switching function"
                        else
                            echo "  WARNING: JS missing version switching function"
                        fi
                        ;;
                esac
            fi
        else
            echo "$asset missing!"
            missing_assets+=("$asset")
        fi
    done
    
    if [ ${#missing_assets[@]} -gt 0 ]; then
        echo "ERROR: Missing shared assets: ${missing_assets[*]}"
        return 1
    fi
    
    return 0
}

# Function to verify root index.html
verify_root_index() {
    local docs_dir="$1"
    local verbose="$2"
    local root_index="$docs_dir/index.html"
    
    echo ""
    echo "=== ROOT INDEX VERIFICATION ==="
    
    if [ -f "$root_index" ]; then
        echo "Root index.html exists"
        
        # Check template type
        if grep -q "Auto-redirecting" "$root_index" && ! grep -q "redoc-container" "$root_index"; then
            echo "Root index.html has CORRECT landing page template"
        else
            echo "ERROR: Root index.html has WRONG template"
            if [ "$verbose" = "true" ]; then
                echo "  Contains Auto-redirecting: $(grep -q "Auto-redirecting" "$root_index" && echo "YES" || echo "NO")"
                echo "  Contains redoc-container: $(grep -q "redoc-container" "$root_index" && echo "YES" || echo "NO")"
            fi
            return 1
        fi
        
        # Check shared asset links
        if grep -q 'href="styles.css"' "$root_index"; then
            echo "Root correctly uses shared CSS"
        else
            echo "ERROR: Root missing shared CSS link"
            return 1
        fi
        
        if grep -q 'src="scripts.js"' "$root_index"; then
            echo "Root correctly uses shared JS"
        else
            echo "ERROR: Root missing shared JS link"
            return 1
        fi
        
    else
        echo "ERROR: Root index.html missing!"
        return 1
    fi
    
    return 0
}

# Function to verify versions.json
verify_versions_json() {
    local docs_dir="$1"
    local verbose="$2"
    local versions_file="$docs_dir/versions.json"
    
    echo ""
    echo "=== VERSIONS.JSON VERIFICATION ==="
    
    if [ -f "$versions_file" ]; then
        echo "Root versions.json exists"
        
        if [ "$verbose" = "true" ]; then
            echo "versions.json content:"
            cat "$versions_file"
        fi
        
        # Validate JSON format
        if ! python3 -m json.tool "$versions_file" >/dev/null 2>&1; then
            echo "ERROR: versions.json contains invalid JSON"
            return 1
        fi
        
    else
        echo "ERROR: Root versions.json missing!"
        return 1
    fi
    
    return 0
}

# Function to verify individual version directory
verify_version_directory() {
    local docs_dir="$1"
    local version="$2"
    local verbose="$3"
    local version_dir="$docs_dir/$version"
    
    echo "Checking version: $version"
    
    # Check index.html
    if [ -f "$version_dir/index.html" ]; then
        # Verify template type
        if grep -q "redoc-container" "$version_dir/index.html" && ! grep -q "Auto-redirecting" "$version_dir/index.html"; then
            echo "  $version/index.html has CORRECT Redoc template"
        else
            echo "  ERROR: $version/index.html has WRONG template!"
            if [ "$verbose" = "true" ]; then
                echo "    First 100 chars:"
                head -c 100 "$version_dir/index.html"
                echo ""
                echo "    Contains redoc-container: $(grep -q "redoc-container" "$version_dir/index.html" && echo "YES" || echo "NO")"
                echo "    Contains Auto-redirecting: $(grep -q "Auto-redirecting" "$version_dir/index.html" && echo "YES" || echo "NO")"
            fi
            return 1
        fi
        
        # Check shared asset links
        if grep -q 'href="../styles.css"' "$version_dir/index.html"; then
            echo "  $version correctly uses shared CSS"
        else
            echo "  ERROR: $version missing shared CSS link"
            return 1
        fi
        
        if grep -q 'src="../scripts.js"' "$version_dir/index.html"; then
            echo "  $version correctly uses shared JS"
        else
            echo "  ERROR: $version missing shared JS link"
            return 1
        fi
        
    else
        echo "  ERROR: $version/index.html missing!"
        return 1
    fi
    
    # Check versions.json
    if [ -f "$version_dir/versions.json" ]; then
        echo "  $version/versions.json exists"
        
        if [ "$verbose" = "true" ]; then
            # Validate JSON format
            if ! python3 -m json.tool "$version_dir/versions.json" >/dev/null 2>&1; then
                echo "    WARNING: $version/versions.json contains invalid JSON"
            fi
        fi
    else
        echo "  ERROR: $version/versions.json missing!"
        return 1
    fi
    
    # Check for OpenAPI spec
    if [ -f "$version_dir/openapi.json" ]; then
        echo "  $version/openapi.json exists"
    else
        echo "  WARNING: $version/openapi.json missing"
    fi
    
    return 0
}

# Function to verify all version directories
verify_version_directories() {
    local docs_dir="$1"
    local verbose="$2"
    
    echo ""
    echo "=== VERSION DIRECTORIES VERIFICATION ==="
    
    local error_count=0
    local version_count=0
    
    for version_dir in "$docs_dir"/*/; do
        if [ -d "$version_dir" ]; then
            local version=$(basename "$version_dir")
            
            # Only check valid version directories
            if is_valid_version "$version"; then
                version_count=$((version_count + 1))
                
                if ! verify_version_directory "$docs_dir" "$version" "$verbose"; then
                    error_count=$((error_count + 1))
                fi
            else
                if [ "$verbose" = "true" ]; then
                    echo "Skipping non-version directory: $version"
                fi
            fi
        fi
    done
    
    echo ""
    echo "Verified $version_count version directories with $error_count errors"
    
    if [ $error_count -gt 0 ]; then
        return 1
    fi
    
    return 0
}

# Function to show documentation structure
show_structure() {
    local docs_dir="$1"
    
    echo "=== FINAL DOCUMENTATION STRUCTURE WITH SHARED ASSETS ==="
    find "$docs_dir" -name "*.html" -o -name "*.json" -o -name "*.css" -o -name "*.js" -o -name "*.png" | sort
    echo ""
}

# Main verification function
main() {
    local docs_dir="docs"
    local verbose="false"
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --docs-dir)
                docs_dir="$2"
                shift 2
                ;;
            --verbose)
                verbose="true"
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
    
    # Check if docs directory exists
    if [ ! -d "$docs_dir" ]; then
        echo "ERROR: Documentation directory '$docs_dir' does not exist"
        exit 1
    fi
    
    echo "Verifying documentation structure in: $docs_dir"
    echo ""
    
    # Show structure overview
    show_structure "$docs_dir"
    
    local total_errors=0
    
    # Verify shared assets
    if ! verify_shared_assets "$docs_dir" "$verbose"; then
        total_errors=$((total_errors + 1))
    fi
    
    # Verify root index.html
    if ! verify_root_index "$docs_dir" "$verbose"; then
        total_errors=$((total_errors + 1))
    fi
    
    # Verify versions.json
    if ! verify_versions_json "$docs_dir" "$verbose"; then
        total_errors=$((total_errors + 1))
    fi
    
    # Verify version directories
    if ! verify_version_directories "$docs_dir" "$verbose"; then
        total_errors=$((total_errors + 1))
    fi
    
    echo ""
    echo "=== VERIFICATION SUMMARY ==="
    if [ $total_errors -eq 0 ]; then
        echo "All verification checks passed successfully!"
        echo "Documentation structure is valid and ready for deployment."
        exit 0
    else
        echo "Verification failed with $total_errors error(s)."
        echo "Please fix the issues above before deployment."
        exit 1
    fi
}

# Run main function if script is executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi