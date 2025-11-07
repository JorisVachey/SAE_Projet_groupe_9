window.onload = function() {
    const faitMaison = document.querySelector('.fait_maison');
    faitMaison.style.opacity = 1;
    faitMaison.style.transform = 'scale(1)';

    const cercle = document.querySelector('.cercle');
    cercle.style.opacity = 1;
    cercle.style.transform = 'scale(1)';
    
    
      setTimeout(() => {
        const header = document.querySelector('header');
        header.style.opacity = 1;
        header.style.transform = 'translateY(0)';
      }, 500);
}