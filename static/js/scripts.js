function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const content = document.getElementById("content");
    const overlay = document.getElementById("overlay");
    const isOpen = sidebar.classList.toggle("open");

    content.classList.toggle("sidebar-open", isOpen);
    overlay.classList.toggle("show", isOpen);
  }

  // Закрытие сайдбара при клике вне его
  overlay.addEventListener('click', function() {
    toggleSidebar();
  });