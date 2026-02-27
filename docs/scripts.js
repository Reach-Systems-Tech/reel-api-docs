/* Shared JavaScript for Reach Systems API Documentation */

/**
 * Populate the version dropdown and wire up version switching.
 * Called once versions.json is loaded.
 */
function populateVersions(versions, currentVersion) {
    var select = document.getElementById('version-select');
    if (!select) return;

    select.innerHTML = '';
    versions.forEach(function (v) {
        var opt = document.createElement('option');
        opt.value = v;
        opt.textContent = v;
        if (v === currentVersion) opt.selected = true;
        select.appendChild(opt);
    });
}

/**
 * Navigate to a different version's docs.
 * Uses simple relative navigation: up one level, into the new version folder.
 */
function switchVersion(newVersion, currentVersion) {
    if (newVersion === currentVersion) return;
    window.location.href = '../' + newVersion + '/';
}

/**
 * Load versions.json and populate the dropdown.
 * Tries ../versions.json first (version subdir), then ./versions.json (root).
 */
function loadVersions(currentVersion) {
    var paths = ['../versions.json', './versions.json'];

    function tryNext(i) {
        if (i >= paths.length) {
            console.log('versions.json not found, using current version only');
            return;
        }
        fetch(paths[i])
            .then(function (r) {
                if (!r.ok) throw new Error(r.status);
                return r.json();
            })
            .then(function (versions) {
                populateVersions(versions, currentVersion);
            })
            .catch(function () {
                tryNext(i + 1);
            });
    }

    tryNext(0);
}

/**
 * Landing page: load versions.json dynamically and render the version list + redirect.
 */
function setupLandingPage() {
    fetch('versions.json')
        .then(function (r) {
            if (!r.ok) throw new Error(r.status);
            return r.json();
        })
        .then(function (versions) {
            renderLandingVersions(versions);
        })
        .catch(function () {
            document.getElementById('version-list').innerHTML =
                '<li class="loading">Could not load versions.json</li>';
            document.getElementById('redirect-banner').innerHTML =
                '<strong>Could not determine latest version.</strong>';
        });
}

function renderLandingVersions(versions) {
    var list = document.getElementById('version-list');
    var banner = document.getElementById('redirect-banner');
    var latest = versions[0];

    // Redirect banner with countdown
    banner.innerHTML =
        '<strong>Auto-redirecting to latest version (' + latest + ') in ' +
        '<span id="countdown">30</span> seconds...</strong><br>' +
        '<a href="' + latest + '/">Go to ' + latest + ' now \u2192</a>';

    var seconds = 30;
    var countdownEl = document.getElementById('countdown');
    var timer = setInterval(function () {
        seconds--;
        if (countdownEl) countdownEl.textContent = seconds;
        if (seconds <= 0) {
            clearInterval(timer);
            window.location.href = latest + '/';
        }
    }, 1000);

    // Version list
    list.innerHTML = '';
    versions.forEach(function (v, i) {
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = v + '/';
        a.textContent = i === 0 ? v + ' (latest)' : v;
        if (i === 0) a.classList.add('latest');
        li.appendChild(a);
        list.appendChild(li);
    });
}