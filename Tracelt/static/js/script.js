document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeSelect = document.getElementById('theme-select');
    const body = document.body;

    // Function to set theme
    function setTheme(theme) {
        if (theme === 'dark') {
            body.classList.add('dark');
            themeToggle.textContent = '☀️';
        } else {
            body.classList.remove('dark');
            themeToggle.textContent = '🌙';
        }
        localStorage.setItem('theme', theme);
    }

    // Function to apply theme based on selection
    function applyTheme() {
        const selected = themeSelect.value;
        if (selected === 'auto') {
            localStorage.removeItem('theme');
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            setTheme(prefersDark ? 'dark' : 'light');
        } else {
            setTheme(selected);
        }
    }

    // Initialize theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        themeSelect.value = savedTheme;
        setTheme(savedTheme);
    } else {
        themeSelect.value = 'auto';
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(prefersDark ? 'dark' : 'light');
    }

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (themeSelect.value === 'auto') {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });

    // Theme select change
    themeSelect.addEventListener('change', applyTheme);

    // Toggle button (for quick toggle)
    themeToggle.addEventListener('click', function() {
        const currentTheme = body.classList.contains('dark') ? 'dark' : 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        themeSelect.value = newTheme;
        setTheme(newTheme);
    });
});