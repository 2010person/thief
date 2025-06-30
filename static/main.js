document.addEventListener("DOMContentLoaded", function() {
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
});