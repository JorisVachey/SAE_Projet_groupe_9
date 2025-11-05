const header = document.querySelector('header');
const sousMenu = document.querySelector('.menu');

function updateMenuHeight() {
    const isMobile = window.innerWidth <= 600;
    if (isMobile) {
        const headerHeight = header.getBoundingClientRect().height;
        sousMenu.style.top = `${headerHeight}px`;
    }
}

updateMenuHeight();


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