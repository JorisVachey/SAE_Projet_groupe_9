let selectedUserId = null;

const rows = document.querySelectorAll(".ligne-client");

rows.forEach(row => {
  row.addEventListener("click", () => {
    rows.forEach(r => r.classList.remove("selected"));
    row.classList.add("selected");
    selectedUserId = row.dataset.id;
    console.log("Client sélectionné :", selectedUserId);
  });
});

// Bouton Blacklister
document.getElementById("btnBannir").addEventListener("click", () => {
    if (!selectedUserId) {
        alert("Veuillez sélectionner un client dans le tableau !");
        return;
    }
    window.location.href = `/admin/bannir-cli/${selectedUserId}`; //redirection vers la route (view.py)
});

// Bouton Déblacklister
document.getElementById("btnDebannir").addEventListener("click", () => {
    if (!selectedUserId) {
        alert("Veuillez sélectionner un client dans le tableau !");
        return;
    }
    window.location.href = `/admin/debannir-cli/${selectedUserId}`;
});