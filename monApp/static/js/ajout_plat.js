function afficherForm() {
    const form = document.querySelector("#pop-up-ajout");
    if (!form) return; // protège si l'élément n'existe pas
    form.classList.add("open");
}

function masquerForm() {
    const form = document.querySelector("#pop-up-ajout");
    if (!form) return; // protège si l'élément n'existe pas
    form.classList.remove("open");
}

document.addEventListener('DOMContentLoaded', function() {
    
    const form = document.querySelector("#pop-up-ajout .champs");
    const tableBody = document.getElementById('tableBody');

form.addEventListener('submit', function(event) {
        
        event.preventDefault(); 

        // --- DEBUT DE LA VALIDATION ---
        const nomP = form.querySelector('[name="nomP"]').value;
        const idTP = form.querySelector('[name="idTP"]').value;
        const prixP = form.querySelector('[name="prixP"]').value;
        const stock = form.querySelector('[name="stock"]').value;
        const desc = form.querySelector('[name="desc"]').value;

        // Vérifie si un champ est vide
        if (!nomP || !idTP || !prixP || !stock || !desc) {
            // Vous pouvez afficher une erreur plus claire à l'utilisateur ici
            console.error("Erreur : Tous les champs sont requis.");
            alert("Veuillez remplir tous les champs, y compris le type de plat.");
            return; // Stoppe l'exécution
        }
        // --- FIN DE LA VALIDATION ---

        const formData = new FormData(form);
        const url = form.action;

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.success) {
                ajouterPlatALaListe(data.plat, tableBody);
                masquerForm();
                form.reset();
            } else {
                // Cette ligne affiche l'erreur "Champs manquants"
                console.error("Erreur lors de l'ajout : " + (data.error));
            }
        })
        .catch(error => {
            console.error('Erreur réseau ou fetch:', error);
        });
    });
});

function ajouterPlatALaListe(plat, tableBody) {
    const nouvelleLigne = document.createElement('tr');
    
    nouvelleLigne.dataset.nomPlat = plat.nomP;

    nouvelleLigne.innerHTML = `
        <td>${plat.nomP}</td>
        <td>${plat.type_nom || 'N/A'}</td>
        <td>${plat.prixP} €</td>
        <td>${plat.stockInit}</td>
        <td>${plat.stock}</td>
    `;
    
    tableBody.appendChild(nouvelleLigne);
}