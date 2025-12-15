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

// Bouton valider
document.getElementById("btnBannir").addEventListener("click", () => {
    if (!selectedUserId) {
        alert("Veuillez sélectionner un client dans le tableau !");
        return;
    }
    window.location.href = `/admin/preparer_panier/${selectedUserId}/valider`;
});

// Bouton refuser
document.getElementById("btnDebannir").addEventListener("click", () => {
    if (!selectedUserId) {
        alert("Veuillez sélectionner un client dans le tableau !");
        return;
    }
    window.location.href = `/admin/preparer_panier/${selectedUserId}/supprimer`;
});