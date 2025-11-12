// pages/static/pages/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('Сайт загружен!');
    
    // Пример простой функциональности
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Можно добавить анимации или другие эффекты
            console.log('Переход на: ' + this.textContent);
        });
    });
});