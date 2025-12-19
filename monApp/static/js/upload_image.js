function initDropZone(zoneId, inputId, previewId) {
    const zone = document.getElementById(zoneId);
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    if (!zone || !input) return;

    const openPicker = () => input.click();
    const showPreview = (file) => {
        if (!preview) return;
        if (file && file.type && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = e => {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            preview.src = '';
            preview.style.display = 'none';
        }
    };

    zone.addEventListener('click', openPicker);
    zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.classList.add('dragover');
    });
    zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
    zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            input.files = e.dataTransfer.files;
            showPreview(input.files[0]);
        }
    });

    input.addEventListener('change', () => {
        if (input.files && input.files[0]) {
            showPreview(input.files[0]);
        }
    });
}

// Init when DOM is ready
window.addEventListener('DOMContentLoaded', () => {
    initDropZone('drop-zone-ajout', 'image-ajout', 'preview-ajout');
    initDropZone('drop-zone-modif', 'image-modif', 'preview-modif');
});
