typePlatChoisi = null;
const btnPlatChoisi = document.querySelectorAll(".choix_type_plat");
btnPlatChoisi.forEach(btn => {
    btn.addEventListener("click", () => {
        typePlatChoisi = parseInt(btn.dataset.id);
        const articles = document.querySelectorAll(".derouler article");
        articles.forEach(article => {
            const idPlat = parseInt(article.dataset.idTp);
            const estPlatChoisi = (idPlat === typePlatChoisi);
            let affichage;
            if (estPlatChoisi) {
                affichage = "block";
            } else {
                affichage = "none";
            }
            article.style.display = affichage;
        });
        btnPlatChoisi.forEach(b => {
            b.style.backgroundColor = "";
            b.querySelector("p").style.borderBottom = "";
        });
        btn.style.backgroundColor = "#FFFFFF";
        btn.querySelector("p").style.borderBottom = "solid 0.125em #E84D0E";
    })
});



const btnTrierPrix = document.getElementById("triPrix");
btnTrierPrix.addEventListener("click", () => {
    const container = document.querySelector(".derouler");
    const lstArticles = Array.from(container.querySelectorAll("article"));
    lstArticles.sort((a, b) => {
        const prixA = parseFloat(a.querySelector(".prix").textContent);
        const prixB = parseFloat(b.querySelector(".prix").textContent);
        return prixA - prixB;
    });
    lstArticles.forEach(article => container.appendChild(article));
});



const btnTrierNom = document.getElementById("triNom");
btnTrierNom.addEventListener("click", () => {
    
    const container = document.querySelector(".derouler");
    const lstArticles = Array.from(container.querySelectorAll("article"));
    lstArticles.sort((a, b) => {
        const nomA = a.querySelector(".nom").textContent;
        const nomB = b.querySelector(".nom").textContent;
        if (nomA < nomB) {
            return -1;
        }
        else if (nomA > nomB) {
            return 1;
        }
        else {
            return 0;
        }
    });
    lstArticles.forEach(article => container.appendChild(article));
});



const btnToutPlat = document.getElementById("tout");
const btnPlat = document.querySelectorAll(".choix_type_plat");
btnToutPlat.addEventListener("click", () => {
    typePlatChoisi = null;
    const articles = document.querySelectorAll(".derouler article");
    articles.forEach(article => {
        article.style.display = "block";
    });
    btnPlat.forEach(b => {
        b.style.backgroundColor = "";
        b.querySelector("p").style.borderBottom = "";
    });
});


function effectuerRecherche() {
    let valRecherche = document.getElementById("recherche_bare").value.toLowerCase();
    const articles = document.querySelectorAll(".derouler article");
    articles.forEach(article => {
        const nomPlat = article.querySelector("h5").textContent.toLowerCase();
        const idTp = parseInt(article.dataset.idTp);
        let affichage;
        if ((typePlatChoisi === null || typePlatChoisi === idTp) &&
            nomPlat.includes(valRecherche)) {
            affichage = "block";
        } else {
            affichage = "none";
        }
        article.style.display = affichage;
    })
}

const btnRechercher = document.getElementById("recherche_bouton");
btnRechercher.addEventListener("click", () => {
    effectuerRecherche();
    document.getElementById("recherche_bare").value = "";
});

const inputRecherche = document.getElementById("recherche_bare");
inputRecherche.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        effectuerRecherche();
        document.getElementById("recherche_bare").value = "";
    }
});

inputRecherche.addEventListener("input", () => {
    effectuerRecherche();
});

inputRecherche.addEventListener("blur", () => {
    document.getElementById("recherche_bare").value = "";
});