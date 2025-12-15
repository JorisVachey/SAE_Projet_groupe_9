function modif_quantite() {
    const tableau = document.getElementById('tableau');
    const ligneSelectionnee = tableau.querySelector('tr.selected');

    if (!ligneSelectionnee) {
        alert("Veuillez sélectionner un plat à modifier.");
        return;
    }

    const idPlat = ligneSelectionnee.dataset.idPlat;
    const nomPlat = ligneSelectionnee.dataset.nomPlat;
    // On utilise stockInit comme valeur de référence pour la "Quantité"
    const stockPlat = ligneSelectionnee.dataset.stockPlat; 

    document.getElementById('modif-qte-id-plat').value = idPlat;
    document.getElementById('modif-qte-nomP').value = nomPlat;
    document.getElementById('modif-quantite').value = ""; 

    const form = document.querySelector("#pop-up-modif-quantite");
    if (form) {
        form.classList.add("open");
    }
}

function masquerFormQuantite() {
    const form = document.querySelector("#pop-up-modif-quantite");
    if (form) {
        form.classList.remove("open");
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-modif-quantite');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const idPlat = document.getElementById('modif-qte-id-plat').value;
            const nouvelleQuantite = document.getElementById('modif-quantite').value;

            const tableau = document.getElementById('tableau');
            const ligne = tableau.querySelector(`tr[data-id-plat="${idPlat}"]`);
            if (ligne) {
                const qteReservee = parseInt(ligne.cells[4].textContent);
                if (parseInt(nouvelleQuantite) <= qteReservee) {
                    alert("La quantité doit être supérieure à la quantité réservée.");
                    return;
                }
            }

            fetch('/admin/modifier_quantite_plat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    idP: idPlat,
                    stock: nouvelleQuantite
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const tableau = document.getElementById('tableau');
                    const ligne = tableau.querySelector(`tr[data-id-plat="${idPlat}"]`);
                    if (ligne) {
                        ligne.dataset.stockPlat = nouvelleQuantite;
                        ligne.cells[3].textContent = nouvelleQuantite;
                    }
                    masquerFormQuantite();
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
