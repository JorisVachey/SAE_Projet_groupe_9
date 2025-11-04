const btnHamburger = document.getElementById('btn_hamburger');
const menu = document.getElementById('menu');

const logo = document.getElementById('logo_hamburger');
let toggle = false;
const imgCroix = logo.dataset.croix;
const imgHamburger = logo.dataset.hamburger;

btnHamburger.addEventListener('click', () => {
    menu.classList.toggle('active');
    toggle = !toggle;
    logo.src = toggle ? imgCroix : imgHamburger;
});