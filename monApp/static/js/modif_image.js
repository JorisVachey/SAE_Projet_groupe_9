function modif_image() {
    const tableau = document.getElementById('tableau');
    const ligneSelectionnee = tableau.querySelector('tr.selected');

    if (!ligneSelectionnee) {
        alert("Veuillez sélectionner un plat à modifier.");
        return;
    }

    const idPlat = ligneSelectionnee.dataset.idPlat;
    const nomPlat = ligneSelectionnee.dataset.nomPlat;

    document.getElementById('modif-img-id-plat').value = idPlat;
    document.getElementById('modif-img-nomP').value = nomPlat;

    const form = document.querySelector('#pop-up-modif-image');
    if (form) form.classList.add('open');
}

function masquerFormImage() {
    const form = document.querySelector('#pop-up-modif-image');
    if (form) form.classList.remove('open');
    // Clear selected image and preview
    const fileInput = document.getElementById('image-modif');
    if (fileInput) fileInput.value = '';
    const preview = document.getElementById('preview-modif');
    if (preview) {
        preview.src = '';
        preview.style.display = 'none';
    }
}

window.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-modif-image');
    if (!form) return;

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const idPlat = document.getElementById('modif-img-id-plat').value;
        const fileInput = document.getElementById('image-modif');
        if (!fileInput || !fileInput.files || !fileInput.files[0]) {
            alert("Veuillez sélectionner une image.");
            return;
        }

        const formData = new FormData();
        formData.append('idP', idPlat);
        formData.append('image', fileInput.files[0]);

        fetch('/admin/modifier_image_plat', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Image mise à jour !');
                masquerFormImage();
            } else {
                alert("Erreur : " + (data.error || 'échec de mise à jour'));
            }
        })
        .catch(err => {
            console.error(err);
            alert('Erreur réseau.');
        });
    });
});
