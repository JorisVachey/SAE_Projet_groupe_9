async function chargerPanier() {
    const res = await fetch('/api/panier');
    const items = await res.json();

    const tbody = document.querySelector('#panier tbody');
    tbody.innerHTML = '';

    let totalCommande = 0;

    items.forEach(item => {
        totalCommande += item.total;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.type}</td>
            <td>${item.nom}</td>
            <td>
                <div class="qte-control">
                    <button class="btn moins" data-id="${item.id}">−</button>
                    <input type="number" value="${item.quantite}" min="1" class="qte" data-id="${item.id}">
                    <button class="btn plus" data-id="${item.id}">+</button>
                </div>
            </td>
            <td>${item.prix.toFixed(2)}</td>
            <td>${item.total.toFixed(2)}</td>
            <td><button class="btn-suppr" data-id="${item.id}">🗑️</button></td>
        `;
        tbody.appendChild(tr);
    });

    document.getElementById('commande').textContent = totalCommande.toFixed(2);

    ajouterListeners();
}

function ajouterListeners() {
    document.querySelectorAll('.plus').forEach(btn => {
        btn.addEventListener('click', async () => {
            const id = btn.dataset.id;
            const input = document.querySelector(`.qte[data-id="${id}"]`);
            const newQte = parseInt(input.value) + 1;
            await majQuantite(id, newQte);
        });
    });

    document.querySelectorAll('.moins').forEach(btn => {
        btn.addEventListener('click', async () => {
            const id = btn.dataset.id;
            const input = document.querySelector(`.qte[data-id="${id}"]`);
            const newQte = Math.max(1, parseInt(input.value) - 1);
            await majQuantite(id, newQte);
        });
    });

    document.querySelectorAll('.qte').forEach(input => {
        input.addEventListener('change', async () => {
            await majQuantite(input.dataset.id, parseInt(input.value));
        });
    });

    document.querySelectorAll('.btn-suppr').forEach(btn => {
        btn.addEventListener('click', async () => {
            const id = btn.dataset.id;
            await fetch(`/api/panier/${id}`, { method: 'DELETE' });
            chargerPanier();
        });
    });
}

async function majQuantite(id, quantite) {
    await fetch(`/api/panier/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quantite })
    });
    chargerPanier();
}

chargerPanier();
