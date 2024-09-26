// scripts.js

// Если у вас уже есть функция для переключения сайдбара, вам нужно убедиться, что она не конфликтует с остальным кодом.
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const content = document.getElementById("content");
    const overlay = document.getElementById("overlay");
    const isOpen = sidebar.classList.toggle("open");

    // Для корректировки содержимого при открытии сайдбара
    content.classList.toggle("sidebar-open", isOpen);
    overlay.classList.toggle("show", isOpen);
}

// Закрытие сайдбара при клике вне его
document.getElementById('overlay').addEventListener('click', function() {
    toggleSidebar();
});
