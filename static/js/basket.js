document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-btn');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const confirmDelete = confirm("Are you sure you want to remove this item from your basket?");
            if (!confirmDelete) {
                event.preventDefault(); // Prevent the default action if not confirmed
            }
        });
    });
});

document.getElementById("increase-btn").addEventListener("click", function() {
    const quantityInput = document.getElementById("quantity");
    quantityInput.value = parseInt(quantityInput.value) + 1; // Increase quantity
});

document.getElementById("decrease-btn").addEventListener("click", function() {
    const quantityInput = document.getElementById("quantity");
    if (parseInt(quantityInput.value) > 1) { // Prevent going below 1
        quantityInput.value = parseInt(quantityInput.value) - 1; // Decrease quantity
    }
});
