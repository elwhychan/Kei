document.addEventListener('DOMContentLoaded', () => {
    const profileButton = document.getElementById('profile-button');
    const profilePopup = document.getElementById('profile-popup');
    const closeProfileButton = profilePopup.querySelector('.close-btn');
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const autoplayVideosToggle = document.getElementById('autoplay-videos');
    const highQualityImagesToggle = document.getElementById('high-quality-images');
    const showCreditsToggle = document.getElementById('show-credits');
    const loginButton = document.getElementById('login-button');

    // --- Fungsi Buka/Tutup Pop-up Profil ---
    if (profileButton && profilePopup && closeProfileButton) {
        profileButton.addEventListener('click', (e) => {
            e.preventDefault();
            profilePopup.style.display = 'flex';
        });

        closeProfileButton.addEventListener('click', () => {
            profilePopup.style.display = 'none';
        });

        profilePopup.addEventListener('click', (e) => {
            if (e.target === profilePopup) {
                profilePopup.style.display = 'none';
            }
        });
    }

    // --- Fungsi untuk Menyimpan dan Memuat Pengaturan ---
    function saveSettings() {
        localStorage.setItem('darkMode', darkModeToggle.checked);
        localStorage.setItem('autoplayVideos', autoplayVideosToggle.checked);
        localStorage.setItem('highQualityImages', highQualityImagesToggle.checked);
        localStorage.setItem('showCredits', showCreditsToggle.checked);
    }

    function loadSettings() {
        // Mode Gelap
        const isDarkMode = localStorage.getItem('darkMode') === 'true';
        darkModeToggle.checked = isDarkMode;
        if (isDarkMode) {
            document.body.classList.add('dark-mode');
        }

        // Pengaturan Lainnya
        autoplayVideosToggle.checked = localStorage.getItem('autoplayVideos') === 'true';
        highQualityImagesToggle.checked = localStorage.getItem('highQualityImages') === 'true';
        showCreditsToggle.checked = localStorage.getItem('showCredits') === 'true';
    }

    // Listeners untuk pengaturan
    darkModeToggle.addEventListener('change', () => {
        document.body.classList.toggle('dark-mode', darkModeToggle.checked);
        saveSettings();
    });
    autoplayVideosToggle.addEventListener('change', saveSettings);
    highQualityImagesToggle.addEventListener('change', saveSettings);
    showCreditsToggle.addEventListener('change', saveSettings);

    loadSettings();

    // --- Mengelola Status Login/Logout ---
    function checkLoginStatus() {
        const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';

        const newLoginButton = loginButton.cloneNode(true);
        loginButton.parentNode.replaceChild(newLoginButton, loginButton);

        if (isLoggedIn) {
            newLoginButton.textContent = 'Keluar';
            newLoginButton.classList.add('logout');
            newLoginButton.addEventListener('click', () => {

                window.location.href = "logout";
            });
        } else {
            newLoginButton.textContent = 'Masuk / Daftar';
            newLoginButton.classList.remove('logout');
            newLoginButton.addEventListener('click', () => {
                // Redirect ke rute login di Flask
                window.location.href = "login";
            });
        }
    }

    checkLoginStatus();
});

