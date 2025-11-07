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
    
    nouvelleLigne.dataset.nomPlat = plat.nom;

    nouvelleLigne.innerHTML = `
        <td>${plat.nom}</td>
        <td>${plat.type_nom || 'N/A'}</td>
        <td>${plat.prix} €</td>
    `;
    
    tableBody.appendChild(nouvelleLigne);
}