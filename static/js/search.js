document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.search-input');
    searchInput.addEventListener('focus', () => {
        searchInput.style.borderColor = '#007BFF';
    });

    searchInput.addEventListener('blur', () => {
        searchInput.style.borderColor = '#ccc';
    });

    // Optional: Smooth scroll to search results on search submit
    const searchForm = document.querySelector('.search-form');
    searchForm.addEventListener('submit', function (e) {
        window.scrollTo({
            top: document.querySelector('.search-results').offsetTop,
            behavior: 'smooth'
        });
    });
});
