document.addEventListener("DOMContentLoaded", () => {
    // Add active class to current nav item
    const currentLocation = location.pathname;
    const navItems = document.querySelectorAll(".nav-item");
    navItems.forEach(item => {
        if(item.getAttribute("href") === currentLocation){
            item.classList.add("active");
        }
    });

    // Smooth page transitions
    navItems.forEach(item => {
        item.addEventListener("click", function(e) {
            e.preventDefault();
            const target = this.getAttribute("href");
            const mainContent = document.querySelector(".main-content");
            if (mainContent) {
                mainContent.style.transition = "all 0.3s ease";
                mainContent.style.opacity = "0";
                mainContent.style.transform = "translateY(20px)";
                
                setTimeout(() => {
                    window.location.href = target;
                }, 300);
            } else {
                window.location.href = target;
            }
        });
    });

    // Theme toggle logic
    const themeToggleBtn = document.getElementById("theme-toggle-btn");
    const currentTheme = localStorage.getItem("theme");

    if (currentTheme === "dark") {
        document.body.classList.add("dark-theme");
        if (themeToggleBtn) themeToggleBtn.innerHTML = "☀️ Aydınlık Mod";
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", () => {
            document.body.classList.toggle("dark-theme");
            let theme = "light";
            if (document.body.classList.contains("dark-theme")) {
                theme = "dark";
                themeToggleBtn.innerHTML = "☀️ Aydınlık Mod";
            } else {
                themeToggleBtn.innerHTML = "🌙 Karanlık Mod";
            }
            localStorage.setItem("theme", theme);
        });
    }
});
