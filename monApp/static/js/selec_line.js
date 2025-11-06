document.addEventListener('DOMContentLoaded', () => {

    const tableau = document.getElementById('tableau');
    const tableBody = document.getElementById('tableBody');
    // Correspond à votre HTML id="btn_suppr"
    const btnSuppr = document.getElementById('btn_suppr');

    if (!btnSuppr) {
        console.error("Erreur: Bouton 'btn_suppr' introuvable !");
        return;
    }

    // ÉCOUTEUR 1 : Gère la sélection des lignes
    tableBody.addEventListener('click', (event) => {
        const ligneCliquee = event.target.closest('tr');
        if (!ligneCliquee) return;

        const ligneActuelle = tableau.querySelector('tr.selected');
        if (ligneActuelle) {
            ligneActuelle.classList.remove('selected');
        }
        ligneCliquee.classList.add('selected');
    });

    // ÉCOUTEUR 2 : Gère le clic sur le bouton (séparé)
    btnSuppr.addEventListener('click', () => {
        
        const ligneSelectionnee = tableau.querySelector('tr.selected');
        
        if (!ligneSelectionnee) {
            alert("Veuillez sélectionner un plat à supprimer.");
            return;
        }

        // CORRECTION :
        // 'dataset.nomPlat' (camelCase) lit 'data-nom-plat' (kebab-case)
        const nomPlat = ligneSelectionnee.dataset.nomPlat; 

        // Sécurité pour arrêter si c'est toujours 'undefined'
        if (!nomPlat) {
            console.error("Erreur: 'nomPlat' est undefined. Vérifiez 'data-nom-plat' dans le HTML.");
            alert("Erreur : Impossible de lire le nom du plat.");
            return;
        }

        fetch(`/supprimer-plat/${nomPlat}`, {
            method: 'DELETE' 
        })
        .then(response => {
            // CORRECTION : Gérer la réponse .json()
            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }
            return response.json();
        })
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