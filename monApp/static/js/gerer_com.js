let selectedUserId = null;

const rows = document.querySelectorAll(".ligne-com");

rows.forEach(row => {
  row.addEventListener("click", () => {
    rows.forEach(r => r.classList.remove("selected"));
    row.classList.add("selected");
    selectedUserId = row.dataset.id;
    console.log("commande sélectionné :", selectedUserId);
  });
});

/**
 * Fonction pour créer et soumettre un formulaire POST dynamiquement.
 * @param {string} action La route Flask à appeler (ex: valider, supprimer).
 */
function submitAdminAction(action) {
    if (!selectedUserId) {
        alert("Veuillez sélectionner un client dans le tableau !");
        return;
    }
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/admin/preparer_panier/${selectedUserId}/${action}`;
    document.body.appendChild(form);
    form.submit();
}

// Bouton valider
document.getElementById("btnBannir").addEventListener("click", () => {
    submitAdminAction('valider');
});

// Bouton refuser
document.getElementById("btnDebannir").addEventListener("click", () => {
    submitAdminAction('supprimer');
});

document.querySelectorAll('.plat-checkbox').forEach(box => {
    box.addEventListener('change', (e) => {
        // 1. Récupérer l'ID de la commande via la ligne du tableau (tr)
        const row = e.target.closest('tr');
        const idR = row.dataset.id;

        // 2. Si la case est cochée, on envoie la requête
        if (e.target.checked) {
            fetch("/admin/update_statut_preparation", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ idR: idR })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log(`Commande ${idR} passée EN PREPARATION`);
                    
                    // (Optionnel) Ajout d'un effet visuel pour dire "C'est en cours"
                    // Par exemple, on met une bordure orange à la ligne
                    row.style.borderLeft = "5px solid orange";
                }
            })
            .catch(error => console.error("Erreur:", error));
        }
    });

    // Empêcher la sélection de la ligne quand on clique sur la checkbox
    box.addEventListener('click', (e) => {
        e.stopPropagation();
    });
});