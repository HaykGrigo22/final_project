document.addEventListener('DOMContentLoaded', function () {
    const carousel = document.querySelector('.product-carousel');

    // Scroll to the right on hover or by button click
    let isScrolling;

    carousel.addEventListener('mouseenter', () => {
        isScrolling = setInterval(() => {
            carousel.scrollBy({ left: 5, behavior: 'smooth' });
        }, 30);
    });

    carousel.addEventListener('mouseleave', () => {
        clearInterval(isScrolling);
    });
});
