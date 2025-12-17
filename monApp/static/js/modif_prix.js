function modif_prix() {
    const tableau = document.getElementById('tableau');
    const ligneSelectionnee = tableau.querySelector('tr.selected');

    if (!ligneSelectionnee) {
        alert("Veuillez sélectionner un plat à modifier.");
        return;
    }

    const idPlat = ligneSelectionnee.dataset.idPlat;
    const nomPlat = ligneSelectionnee.dataset.nomPlat;
    const prixPlat = ligneSelectionnee.dataset.prixPlat;

    document.getElementById('modif-id-plat').value = idPlat;
    document.getElementById('modif-nomP').value = nomPlat;
    document.getElementById('modif-prix').value = "";

    const form = document.querySelector("#pop-up-modif-prix");
    if (form) {
        form.classList.add("open");
    }
}

function masquerFormPrix() {
    const form = document.querySelector("#pop-up-modif-prix");
    if (form) {
        form.classList.remove("open");
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-modif-prix');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const idPlat = document.getElementById('modif-id-plat').value;
            const nouveauPrix = document.getElementById('modif-prix').value;

            fetch('/admin/modifier_prix_plat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    idP: idPlat,
                    prixP: nouveauPrix
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const tableau = document.getElementById('tableau');
                    const ligne = tableau.querySelector(`tr[data-id-plat="${idPlat}"]`);
                    if (ligne) {
                        const prixFormate = parseFloat(nouveauPrix).toFixed(2);
                        ligne.dataset.prixPlat = prixFormate;
                        ligne.cells[2].textContent = prixFormate + '€';
                    }
                    masquerFormPrix();
                } else {
                    alert("Erreur lors de la modification : " + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Une erreur est survenue.");
            });
        });
    }
});
