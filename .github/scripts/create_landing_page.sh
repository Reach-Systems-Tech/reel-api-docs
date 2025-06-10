#!/bin/bash
#
# File: create_landing_page.sh
# Title: Landing Page Generator
# Company: Reach Systems Ltd
# Author: Zeke Critchlow
# Date: June 5th, 2025
# Description: Creates the root index.html landing page with shared assets
#

set -e  # Exit on any error

# Function to show usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --latest-version VERSION    Latest version for redirect and links"
    echo "  --api-title TITLE          API title for the page (optional)"
    echo "  --force                    Overwrite existing index.html"
    echo "  --help                     Show this help message"
    exit 1
}

# Function to extract API title from version-specific file
extract_api_title() {
    local latest_version="$1"
    local version_file="docs/$latest_version/index.html"
    
    if [ -f "$version_file" ]; then
        # Extract title from version file
        local extracted_title=$(grep -o '<title>[^<]*</title>' "$version_file" | sed 's/<title>\(.*\) - .*/\1/' | head -1 2>/dev/null || echo "")
        extracted_title=$(echo "$extracted_title" | sed 's/<[^>]*>//g' | sed 's/Documentation.*//' | xargs)
        
        if [ -n "$extracted_title" ]; then
            echo "$extracted_title"
        else
            echo "API Documentation"
        fi
    else
        echo "API Documentation"
    fi
}

# Function to verify shared asset links in generated file
verify_landing_page_assets() {
    local output_file="$1"
    
    echo "Verifying shared asset links in landing page..."
    
    # Check CSS link
    if grep -q 'href="styles.css"' "$output_file"; then
        echo "  Root correctly links to shared CSS"
    else
        echo "  ERROR: Root missing shared CSS link"
        return 1
    fi
    
    # Check JS link
    if grep -q 'src="scripts.js"' "$output_file"; then
        echo "  Root correctly links to shared JS"
    else
        echo "  ERROR: Root missing shared JS link"
        return 1
    fi
    
    # Check for landing page template markers
    if grep -q "Auto-redirecting" "$output_file"; then
        echo "  Landing page contains correct redirect functionality"
    else
        echo "  WARNING: Landing page missing auto-redirect text"
    fi
    
    return 0
}

# Function to create the landing page HTML
create_landing_page_html() {
    local latest_version="$1"
    local api_title="$2"
    local output_file="$3"
    
    echo "Creating landing page HTML..."
    echo "  Latest version: $latest_version"
    echo "  API title: $api_title"
    echo "  Output file: $output_file"
    
    # Create the HTML file
    cat > "$output_file" << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$api_title Documentation</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body class="landing-page">
    <div class="landing-container">
        <h1>$api_title Documentation</h1>
        
        <div class="auto-redirect">
            <p><strong>Auto-redirecting to latest version ($latest_version) in 10 seconds...</strong></p>
            <p><a href="$latest_version/">Click here to go immediately</a></p>
        </div>
        
        <div class="features">
            <h3>Enhanced with Redoc</h3>
            <ul>
                <li><strong>Built-in sidebar navigation</strong> - Easy browsing of endpoints</li>
                <li><strong>Search functionality</strong> - Find endpoints and schemas quickly</li>
                <li><strong>Three-panel layout</strong> - Description, examples, and schemas</li>
                <li><strong>Responsive design</strong> - Works great on all devices</li>
                <li><strong>Static documentation</strong> - Perfect for hardware systems</li>
            </ul>
        </div>
        
        <h2>Available Versions</h2>
        <ul class="version-list">
            <li><a href="$latest_version/" class="latest">$latest_version (latest)</a></li>
        </ul>
    </div>
    
    <script src="scripts.js"></script>
    <script>
        setupAutoRedirect('$latest_version');
    </script>
</body>
</html>
EOF
    
    echo "  Landing page HTML created successfully"
}

# Function to check if landing page should be created
should_create_landing_page() {
    local force="$1"
    local output_file="docs/index.html"
    
    if [ "$force" = "true" ]; then
        echo "Force flag set - will overwrite existing index.html"
        return 0
    fi
    
    if [ ! -f "$output_file" ]; then
        echo "Root index.html does not exist - will create new one"
        return 0
    else
        echo "Root index.html already exists - will verify links only"
        return 1
    fi
}

# Function to verify existing landing page
verify_existing_landing_page() {
    local output_file="docs/index.html"
    
    echo "Verifying existing root index.html..."
    
    # Check if it has correct shared asset links
    if grep -q 'href="styles.css"' "$output_file"; then
        echo "  Existing root correctly links to shared CSS"
    else
        echo "  WARNING: Existing root may need shared CSS link update"
    fi
    
    if grep -q 'src="scripts.js"' "$output_file"; then
        echo "  Existing root correctly links to shared JS"
    else
        echo "  WARNING: Existing root may need shared JS link update"
    fi
}

# Main function
main() {
    local latest_version=""
    local api_title=""
    local force="false"
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --latest-version)
                latest_version="$2"
                shift 2
                ;;
            --api-title)
                api_title="$2"
                shift 2
                ;;
            --force)
                force="true"
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
    if [ -z "$latest_version" ]; then
        echo "Error: --latest-version is required"
        usage
    fi
    
    # Auto-extract API title if not provided
    if [ -z "$api_title" ]; then
        echo "No API title provided, extracting from version file..."
        api_title=$(extract_api_title "$latest_version")
        echo "Extracted API title: '$api_title'"
    fi
    
    local output_file="docs/index.html"
    
    echo "Creating root landing page index.html with shared assets..."
    
    # Check if we should create the landing page
    if should_create_landing_page "$force"; then
        # Ensure docs directory exists
        mkdir -p docs
        
        # Create the landing page
        create_landing_page_html "$latest_version" "$api_title" "$output_file"
        
        # Verify the created file
        verify_landing_page_assets "$output_file"
        
        echo "Landing page created successfully at $output_file"
    else
        # Just verify existing file
        verify_existing_landing_page
        echo "Existing landing page verified"
    fi
}

# Run main function if script is executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi