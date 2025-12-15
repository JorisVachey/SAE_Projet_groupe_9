document.addEventListener('DOMContentLoaded', () => {

    const tableau = document.getElementById('tableau');
    const tableBody = document.getElementById('tableBody');
    const btnSuppr = document.getElementById('btn_suppr');

    tableBody.addEventListener('click', (event) => {
        const ligneCliquee = event.target.closest('tr');
        if (!ligneCliquee) return;

        const ligneActuelle = tableau.querySelector('tr.selected');
        if (ligneActuelle) {
            ligneActuelle.classList.remove('selected');
        }
        ligneCliquee.classList.add('selected');
    });

    btnSuppr.addEventListener('click', () => {
        
        const ligneSelectionnee = tableau.querySelector('tr.selected');
        
        if (!ligneSelectionnee) {
            alert("Veuillez sélectionner un plat à supprimer.");
            return;
        }
        if (!confirm("Êtes-vous sûr de vouloir supprimer ce plat ?")) {
            return;
        }
        const nomPlat = ligneSelectionnee.dataset.nomPlat; 

        fetch(`/supprimer-plat/${nomPlat}`, {
            method: 'DELETE' 
        })
        .then(response => {
            return response.json()})
        .then(data => {
            if (data.success) {
                ligneSelectionnee.remove();
            } else {
                alert("Erreur lors de la suppression : " + data.error);
            }
        })
        .catch(error => {
            console.error('Erreur réseau ou fetch:', error);
            alert("Erreur de connexion avec le serveur.");
        });
    });

});