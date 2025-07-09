document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.getElementById('togglePassword');
    const password = document.getElementById('password');
    if (togglePassword && password) {
        togglePassword.addEventListener('click', function () {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
        });
    }

    const audio = document.getElementById('bgm');
    if (audio) {
        audio.play().catch(() => {
            document.addEventListener('click', function playOnce() {
                audio.play();
                document.removeEventListener('click', playOnce);
            });
        });
    }

    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        setTimeout(function () {
            loadingScreen.style.opacity = 0;
            setTimeout(function () {
                loadingScreen.style.display = 'none';
            }, 500);
        }, 1800);
    }

    function setCookie(name, value, days) {
        const d = new Date();
        d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = name + "=" + value + ";path=/;expires=" + d.toUTCString();
    }

    function getCookie(name) {
        const cookies = document.cookie.split(';').map(c => c.trim());
        for (const c of cookies) {
            if (c.startsWith(name + '=')) return c.substring(name.length + 1);
        }
        return null;
    }

    const banner = document.getElementById('cookie-banner');
    if (banner && !getCookie('cookies_accepted')) {
        banner.style.display = 'block';
    }

    const acceptBtn = document.getElementById('accept-cookies');
    if (acceptBtn) {
        acceptBtn.onclick = () => {
            setCookie('cookies_accepted', 'true', 365);
            if (banner) banner.style.display = 'none';
        };
    }
});