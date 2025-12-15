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