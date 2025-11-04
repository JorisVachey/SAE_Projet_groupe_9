const btnHamburger = document.getElementById('btn_hamburger');
const menu = document.getElementById('menu');

btnHamburger.addEventListener('click', () => {
    menu.classList.toggle('active');
});