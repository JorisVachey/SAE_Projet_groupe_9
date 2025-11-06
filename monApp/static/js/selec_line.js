const tableau = document.getElementById('tableau');
const tableBody = document.getElementById('tableBody'); // Vous avez déjà cet ID

tableBody.addEventListener('click', (event) => {
    const ligneCliquee = event.target.closest('tr');
    if (!ligneCliquee) return;

    const ligneActuelle = tableau.querySelector('tr.selected');

    if (ligneActuelle) {
        ligneActuelle.classList.remove('selected');
    }

    ligneCliquee.classList.add('selected');
    
});