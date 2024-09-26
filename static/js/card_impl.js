// Heart animation
function toggleHeart() {
    const heart = document.querySelector('.heart-icon i');
    heart.classList.toggle('far');  // Empty heart
    heart.classList.toggle('fas');  // Full heart
    document.querySelector('.heart-icon').classList.toggle('active');  // Scaling animation
  }
  
  // Close popup function
  function closePopup() {
    const popup = document.getElementById('popup');
    popup.style.display = 'none';
  }
  