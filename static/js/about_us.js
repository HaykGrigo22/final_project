// Optional JS to add interactivity (about_us.js)
document.querySelectorAll('.team-member').forEach(member => {
    member.addEventListener('click', () => {
        alert(`You clicked on ${member.querySelector('h3').innerText}`);
    });
});
