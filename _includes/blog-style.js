document.addEventListener("DOMContentLoaded", function () {
    // Dark mode toggle
    const toggleBtn = document.getElementById("darkModeToggle");
    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            document.body.classList.toggle("dark-mode");
            toggleBtn.textContent = document.body.classList.contains("dark-mode") ? "☀️" : "🌙 ";
        });
    }

    // Right-click protection
    const message = "Right- Click Function Disabled!";
    document.addEventListener('contextmenu', function (e) {
        try { alert(message); } catch (err) { }
        e.preventDefault();
    });

    // Block some dev tools shortcuts
    document.addEventListener('keydown', function (e) {
        const key = (e.key || '').toUpperCase();
        if (e.key === 'F12' || e.keyCode === 123) { e.preventDefault(); return false; }
        if (e.ctrlKey && e.shiftKey && (key === 'I' || key === 'J' || key === 'C')) { e.preventDefault(); return false; }
        if (e.ctrlKey && key === 'U') { e.preventDefault(); return false; }
    });

    // Old browser selection disable
    function disableselect() { return false; }
    function reEnable() { return true; }
    document.onselectstart = disableselect;
    if (window.sidebar) {
        document.onmousedown = disableselect;
        document.onclick = reEnable;
    }

    // Back-to-top button
    const mybutton = document.getElementById("myBtn");
    window.onscroll = function () {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            mybutton.style.display = "block";
        } else {
            mybutton.style.display = "none";
        }
    };
    window.topFunction = function () {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    };
});