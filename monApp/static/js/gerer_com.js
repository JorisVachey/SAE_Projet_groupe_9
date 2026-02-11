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

// Fonction pour charger l'état des checkboxes depuis localStorage
function loadCheckboxStates() {
    document.querySelectorAll('.plat-checkbox').forEach(box => {
        const row = box.closest('tr');
        const idR = row.dataset.id;
        const platIndex = Array.from(row.querySelectorAll('.plat-checkbox')).indexOf(box);
        const checkboxKey = `checkbox_${idR}_${platIndex}`;
        
        const savedState = localStorage.getItem(checkboxKey);
        if (savedState === 'true') {
            box.checked = true;
        }
    });
    
    // Vérifier et appliquer les couleurs de bordure après chargement
    rows.forEach(row => {
        const idR = row.dataset.id;
        const allCheckboxes = row.querySelectorAll('.plat-checkbox');
        const checkedCheckboxes = row.querySelectorAll('.plat-checkbox:checked');
        
        if (checkedCheckboxes.length === allCheckboxes.length && allCheckboxes.length > 0) {
            row.style.borderLeft = "5px solid green";
        } else if (checkedCheckboxes.length > 0) {
            row.style.borderLeft = "5px solid orange";
        }
    });
}

// Charger les états au chargement de la page
loadCheckboxStates();

document.querySelectorAll('.plat-checkbox').forEach(box => {
    box.addEventListener('change', (e) => {
        const row = e.target.closest('tr');
        const idR = row.dataset.id;
        
        // Sauvegarder l'état de la checkbox dans localStorage
        const platIndex = Array.from(row.querySelectorAll('.plat-checkbox')).indexOf(box);
        const checkboxKey = `checkbox_${idR}_${platIndex}`;
        localStorage.setItem(checkboxKey, e.target.checked);
        
        // Compter le nombre total de checkboxes et celles cochées pour cette commande
        const allCheckboxes = row.querySelectorAll('.plat-checkbox');
        const checkedCheckboxes = row.querySelectorAll('.plat-checkbox:checked');
        const allChecked = allCheckboxes.length === checkedCheckboxes.length;
        
        fetch("/admin/update_statut_preparation", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ 
                idR: idR, 
                allChecked: allChecked 
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.statut === "PRÊTE") {
                    console.log(`Commande ${idR} est PRÊTE`);
                    row.style.borderLeft = "5px solid green";
                } else if (data.statut === "EN PRÉPARATION") {
                    console.log(`Commande ${idR} EN PRÉPARATION`);
                    row.style.borderLeft = "5px solid orange";
                }
            }
        })
        .catch(error => console.error("Erreur:", error));
    });
    box.addEventListener('click', (e) => {
        e.stopPropagation();
    });
});