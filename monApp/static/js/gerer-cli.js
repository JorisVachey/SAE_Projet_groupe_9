let selectedUserId = null;

const rows = document.querySelectorAll(".ligne-client");

rows.forEach(row => {
  row.addEventListener("click", () => {
    // Supprime 'selected' de TOUTES les lignes
    rows.forEach(r => r.classList.remove("selected"));

    // Ajoute 'selected' uniquement à celle cliquée
    row.classList.add("selected");

    // Mémorise l'ID sélectionné
    selectedUserId = row.dataset.id;

    console.log("Client sélectionné :", selectedUserId);
  });
});

// Bouton Blacklister
document.getElementById("btnBannir").addEventListener("click", () => {
    if (!selectedUserId) {
        alert("Veuillez sélectionner un client dans le tableau !"); // Vérification qu'un client est sélectionné
        return;
    }
    window.location.href = `/admin/bannir-cli/${selectedUserId}`; // Redirection vers la route de blacklisting avec l'ID du client lors du clic sur le bouton
});

// Bouton Déblacklister
document.getElementById("btnDebannir").addEventListener("click", () => {
    if (!selectedUserId) {
        alert("Veuillez sélectionner un client dans le tableau !"); // Vérification qu'un client est sélectionné
        return;
    }
    window.location.href = `/admin/debannir-cli/${selectedUserId}`; // Redirection vers la route de déblacklisting avec l'ID du client lors du clic sur le bouton
});