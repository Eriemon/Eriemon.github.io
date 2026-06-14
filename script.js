// Style Toggle - Academic ↔ Natural
const styleToggle = document.getElementById('styleToggle');
const styleLabel = document.getElementById('styleLabel');
const styleLink = document.getElementById('theme-style');

const STYLES = {
    academic: {
        file: 'style-academic.css',
        name: 'Academic',
        next: 'Natural',
        fonts: 'family=Source+Sans+3:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500'
    },
    natural: {
        file: 'style-natural.css',
        name: 'Natural',
        next: 'Academic',
        fonts: 'family=Fraunces:wght@400;500;600;700&family=Nunito:wght@300;400;500;600;700&family=Fira+Code:wght@400;500'
    }
};

const DEFAULT_STYLE = STYLES.natural.file;
const STYLE_ALIASES = {
    academic: STYLES.academic.file,
    natural: STYLES.natural.file
};

function resolveStoredStyle(styleValue) {
    const normalized = typeof styleValue === 'string' ? styleValue.trim() : '';
    if (!normalized) {
        return DEFAULT_STYLE;
    }

    if (normalized === STYLES.academic.file || normalized === STYLES.natural.file) {
        return normalized;
    }

    return STYLE_ALIASES[normalized.toLowerCase()] || DEFAULT_STYLE;
}

// Load saved style or default to Natural, then persist the canonical value.
const savedStyle = resolveStoredStyle(localStorage.getItem('selectedStyle'));
if (styleLink) {
    styleLink.href = savedStyle;
}
localStorage.setItem('selectedStyle', savedStyle);

// Font loading
const googleFontsLink = document.getElementById('google-fonts');

function loadFontsForStyle(styleFile) {
    const style = styleFile.includes('academic') ? STYLES.academic : STYLES.natural;
    if (googleFontsLink) {
        googleFontsLink.href = `https://fonts.googleapis.com/css2?${style.fonts}&display=swap`;
    }
}

loadFontsForStyle(savedStyle);

function updateStyleLabel() {
    const isAcademic = styleLink.href.includes('academic');
    if (styleLabel) {
        styleLabel.textContent = isAcademic ? 'Natural' : 'Academic';
    }
}

updateStyleLabel();

if (styleToggle) {
    styleToggle.addEventListener('click', () => {
        const isAcademic = styleLink.href.includes('academic');
        const newStyle = isAcademic ? STYLES.natural.file : STYLES.academic.file;
        styleLink.href = newStyle;
        localStorage.setItem('selectedStyle', newStyle);
        updateStyleLabel();
        loadFontsForStyle(newStyle);
    });
}

// Theme Toggle (Light/Dark)
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

const savedTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-theme', savedTheme);

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

// Navbar Scroll Effect
const navbar = document.querySelector('.navbar');

function handleNavbarScroll() {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
}

window.addEventListener('scroll', handleNavbarScroll, { passive: true });

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Refresh GitHub metrics from the generated data file while keeping HTML fallbacks usable.
async function loadGithubProjectMetrics() {
    try {
        const response = await fetch('data/github-projects.json', { cache: 'no-store' });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        const summary = data.summary || {};

        ['projects', 'repositories', 'stars'].forEach(statName => {
            const statElement = document.querySelector(`[data-stat="${statName}"]`);
            const value = summary[statName];
            if (statElement && Number.isFinite(value)) {
                statElement.textContent = String(value);
            }
        });

        (data.projects || []).forEach(project => {
            if (!project || !project.name) {
                return;
            }

            const card = document.querySelector(`[data-project="${project.name}"]`);
            if (!card) {
                return;
            }

            ['stars', 'forks', 'clones14d'].forEach(metricName => {
                const metricElement = card.querySelector(`[data-metric="${metricName}"]`);
                const value = project[metricName];
                if (metricElement && Number.isFinite(value)) {
                    metricElement.textContent = String(value);
                }
            });
        });
    } catch (error) {
        console.warn('Unable to load GitHub project metrics; using HTML fallback values.', error);
    }
}

document.addEventListener('DOMContentLoaded', loadGithubProjectMetrics);
