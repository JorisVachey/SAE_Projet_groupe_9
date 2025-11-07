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
        location.reload();
      })
      .catch(err => {
        console.error("Erreur fetch:", err);
      });
  });
});
