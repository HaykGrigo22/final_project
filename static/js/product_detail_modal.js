document.addEventListener('DOMContentLoaded', () => {
    const modals = document.querySelectorAll('.modal');
    const btns = document.querySelectorAll('.btn-buy');
    const spans = document.querySelectorAll('.close');
console.log(btns)
    // Открытие модального окна
    btns.forEach((btn, index) => {
        btn.onclick = function() {
            modals[index].style.display = "block";
        }
    });

    // Закрытие модального окна
    spans.forEach((span, index) => {
        span.onclick = function() {
            modals[index].style.display = "none";
        }
    });

    // Закрытие модального окна при нажатии вне его
    window.onclick = function(event) {
        modals.forEach((modal) => {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        });
    };
});
