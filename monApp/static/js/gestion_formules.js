function afficherForm() {
    const form = document.querySelector("#pop-up-ajout");
    if (!form) return;
    form.classList.add("open");
}

function masquerForm() {
    const popup = document.querySelector("#pop-up-ajout");
    if (!popup) return;
    popup.classList.remove("open");

    const form = document.getElementById('form-ajout-formule');
    if (form) {
        form.reset();
        const details = form.querySelectorAll('details');
        details.forEach(detail => {
            detail.removeAttribute('open');
        });
        const quantityInputs = form.querySelectorAll('.quantite-input');
        quantityInputs.forEach(input => {
            input.disabled = true;
            input.value = 1;
        });
    }
}

function modif_prix() {
    const tableau = document.getElementById('tableau');
    const ligneSelectionnee = tableau.querySelector('tr.selected');

    if (!ligneSelectionnee) {
        alert("Veuillez sélectionner une formule à modifier.");
        return;
    }

    const idFormule = ligneSelectionnee.dataset.idFormule;
    const nomFormule = ligneSelectionnee.dataset.nomFormule;
    
    document.getElementById('modif-id-formule').value = idFormule;
    document.getElementById('modif-nomF').value = nomFormule;
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

function toggleQuantity(checkbox) {
    const container = checkbox.closest('.plat-selection');
    const quantityInput = container.querySelector('.quantite-input');
    if (quantityInput) {
        quantityInput.disabled = !checkbox.checked;
        if (!checkbox.checked) {
            quantityInput.value = 1;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const tableau = document.getElementById('tableau');
    const tableBody = document.getElementById('tableBody');
    const btnSuppr = document.getElementById('btn_suppr');
    const form = document.getElementById('form-ajout-formule');
    const formPrix = document.getElementById('form-modif-prix');

    // Selection logic
    if (tableBody) {
        tableBody.addEventListener('click', (event) => {
            const ligneCliquee = event.target.closest('tr');
            if (!ligneCliquee) return;

            const ligneActuelle = tableau.querySelector('tr.selected');
            if (ligneActuelle) {
                ligneActuelle.classList.remove('selected');
            }
            ligneCliquee.classList.add('selected');
        });
    }

    // Delete logic
    if (btnSuppr) {
        btnSuppr.addEventListener('click', () => {
            const ligneSelectionnee = tableau.querySelector('tr.selected');
            if (!ligneSelectionnee) {
                alert("Veuillez sélectionner une formule à supprimer.");
                return;
            }
            
            if (!confirm("Êtes-vous sûr de vouloir supprimer cette formule ?")) {
                return;
            }

            const idFormule = ligneSelectionnee.dataset.idFormule;

            fetch(`/admin/supprimer-formule/${idFormule}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    ligneSelectionnee.remove();
                } else {
                    alert("Erreur lors de la suppression : " + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Une erreur est survenue.");
            });
        });
    }

    // Add logic
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(form);
            
            // Check if at least one dish is selected
            const plats = formData.getAll('plats');
            if (plats.length === 0) {
                alert("Veuillez sélectionner au moins un plat.");
                return;
            }

            fetch('/admin/gestion_formules/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    masquerForm();
                    window.location.reload();
                } else {
                    alert("Erreur lors de l'ajout : " + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Une erreur est survenue.");
            });
        });
    }

    // Modify price logic
    if (formPrix) {
        formPrix.addEventListener('submit', function(event) {
            event.preventDefault();

            const idFormule = document.getElementById('modif-id-formule').value;
            const nouveauPrix = document.getElementById('modif-prix').value;

            fetch('/admin/modifier_prix_formule', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    idF: idFormule,
                    prixF: nouveauPrix
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const tableau = document.getElementById('tableau');
                    const ligne = tableau.querySelector(`tr[data-id-formule="${idFormule}"]`);
                    if (ligne) {
                        const prixFormate = parseFloat(nouveauPrix).toFixed(2);
                        ligne.dataset.prixFormule = prixFormate;
                        ligne.cells[1].textContent = prixFormate + '€';
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
