function afficherForm() {
    const form = document.querySelector("#pop-up-ajout");
    if (!form) return;
    form.classList.add("open");
}

function masquerForm() {
    const form = document.querySelector("#pop-up-ajout");
    if (!form) return;
    form.classList.remove("open");
    const fileInput = document.getElementById('image-ajout');
    if (fileInput) fileInput.value = '';
    const preview = document.getElementById('preview-ajout');
    if (preview) {
        preview.src = '';
        preview.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    
    const form = document.querySelector("#form-ajout-plat");
    const tableBody = document.getElementById('tableBody');

    form.addEventListener('submit', function(event) {
        
        event.preventDefault(); 

        const nomP = form.querySelector('[name="nomP"]').value;
        const idTP = form.querySelector('[name="idTp"]').value;
        const prixP = form.querySelector('[name="prixP"]').value;
        const stock = form.querySelector('[name="stock"]').value;
        const desc = form.querySelector('[name="desc"]').value;

        if (!nomP || !idTP || !prixP || !stock || !desc) {
            console.error("Erreur : Tous les champs sont requis.");
            alert("Veuillez remplir tous les champs, y compris le type de plat.");
            return;
        }

        const formData = new FormData(form);
        const url = form.action;

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                 return response.json().then(errData => {
                     throw new Error(errData.error || 'Erreur inconnue');
                 });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                ajouterPlatALaListe(data.plat, tableBody);

                form.reset();
                const fileInput = document.getElementById('image-ajout');
                if (fileInput) fileInput.value = '';
                const preview = document.getElementById('preview-ajout');
                if (preview) {
                    preview.src = '';
                    preview.style.display = 'none';
                }
                masquerForm();
            } else {
                console.error("Erreur lors de l'ajout : " + (data.error));
                alert("Erreur : " + data.error);
            }
        })
        .catch(error => {
            console.error('Erreur réseau ou fetch:', error);
            alert("Erreur : " + error.message);
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