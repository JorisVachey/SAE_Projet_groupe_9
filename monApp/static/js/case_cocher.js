document.addEventListener("DOMContentLoaded", function () {
  const checkbox = document.getElementById("checkbox-surplace");
  if (!checkbox) return;
  const idR = checkbox.dataset.idr;
  checkbox.addEventListener("change", function () {
    const surPlace = checkbox.checked;

    fetch("/update_checkbox", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ idR: idR, sur_place: surPlace })
    })
      .then(response => {
        if (!response.ok) throw new Error("Erreur réseau");
        return response.json();
      })
      .then(data => {
        console.log("Serveur:", data.message);
        alert(data.message);
        location.reload();
        if (!data.success) {
            checkbox.checked = false;
            checkbox.disabled = true;
        }
      })
      .catch(err => {
        console.error("Erreur fetch:", err);
      });
  });loadCheckboxStates();

  // Sauvegarder l'état quand on coche/décoche
  document.querySelectorAll('.plat-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
      saveCheckboxStates();
    });
  });

  function saveCheckboxStates() {
    const checkboxStates = {};
    
    document.querySelectorAll('.plat-checkbox').forEach((box, index) => {
      // Créer un identifiant unique pour chaque checkbox
      const tr = box.closest('tr');
      const commandeId = tr.dataset.id;
      const platNom = box.closest('li').textContent.trim();
      const uniqueId = `commande-${commandeId}-${platNom}`;
      
      checkboxStates[uniqueId] = box.checked;
    });
    
    // Sauvegarder dans le localStorage
    localStorage.setItem('checkboxStates', JSON.stringify(checkboxStates));
    console.log('États sauvegardés:', checkboxStates);
  }

  function loadCheckboxStates() {
    const savedStates = localStorage.getItem('checkboxStates');
    
    if (!savedStates) return;
    
    const checkboxStates = JSON.parse(savedStates);
    
    document.querySelectorAll('.plat-checkbox').forEach((box) => {
      const tr = box.closest('tr');
      const commandeId = tr.dataset.id;
      const platNom = box.closest('li').textContent.trim();
      const uniqueId = `commande-${commandeId}-${platNom}`;
      
      if (checkboxStates[uniqueId] !== undefined) {
        box.checked = checkboxStates[uniqueId];
        
        if (box.checked) {
          box.closest('.checkbox-container').querySelector('span').style.textDecoration = 'line-through';
          box.closest('.checkbox-container').querySelector('span').style.opacity = '0.7';
        }
      }
    });
    
    console.log('États restaurés:', checkboxStates);
  }

});

