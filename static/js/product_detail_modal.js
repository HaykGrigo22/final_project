document.addEventListener('DOMContentLoaded', () => {
    const modals = document.querySelectorAll('.popup'); // Select all popups
    const btns = document.querySelectorAll('.btn-buy'); // Select all "Buy Now" buttons
    const closeBtns = document.querySelectorAll('.close-btn'); // Select all close buttons

    // Open the modal for each corresponding "Buy Now" button
    btns.forEach((btn, index) => {
        btn.onclick = function() {
            modals[index].style.display = "flex";
        }
    });

    // Close the modal for each corresponding close button
    closeBtns.forEach((closeBtn, index) => {
        closeBtn.onclick = function() {
            modals[index].style.display = "none";
        }
    });

    // Close the modal when clicking outside the modal content
    window.onclick = function(event) {
        modals.forEach((modal) => {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        });
    }
});
