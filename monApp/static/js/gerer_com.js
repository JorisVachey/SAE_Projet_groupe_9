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
    submitAdminAction('récupérer');
});

// Bouton refuser
document.getElementById("btnDebannir").addEventListener("click", () => {
    submitAdminAction('supprimer');
});

document.querySelectorAll('.plat-checkbox').forEach(box => {
    box.addEventListener('change', (e) => {
        const row = e.target.closest('tr');
        const idR = row.dataset.id;
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
                    row.style.borderLeft = "5px solid orange";
                }
            })
            .catch(error => console.error("Erreur:", error));
        }
    });
    box.addEventListener('click', (e) => {
        e.stopPropagation();
    });
});