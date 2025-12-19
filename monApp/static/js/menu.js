typePlatChoisi = null;

function StockEpuise(article) {
    const stockInput = article.querySelector(".stock");

    if (!stockInput) {
        return false;
    }

    const stock = parseInt(stockInput.value, 10);

    if (stock === 0) {
        return true;
    }
    return false;
}

const articles = document.querySelectorAll(".deux");
articles.forEach(article => {
    if (StockEpuise(article)) {
        article.style.opacity = "0.5";
        article.style.pointerEvents = "none";
        article.style.filter = "grayscale(100%)";
    }
});

const btnPlatChoisi = document.querySelectorAll(".choix_type_plat");
btnPlatChoisi.forEach(btn => {
    btn.addEventListener("click", () => {
        const dataId = btn.dataset.id;
        if (dataId === "formules") {
            typePlatChoisi = dataId;
        } else {
            typePlatChoisi = parseInt(dataId, 10);
        }

        const articles = document.querySelectorAll(".deux");
        articles.forEach(article => {
            const idPlat = article.dataset.idTp;
            let estPlatChoisi;

            if (typePlatChoisi === "formules") {
                estPlatChoisi = article.classList.contains("formule_article");
            } else {
                let identifiantTexte = idPlat;
                let identifiantNombre = parseInt(identifiantTexte, 10);
                let resultatComparaison = (identifiantNombre === typePlatChoisi);
                estPlatChoisi = resultatComparaison;
            }
            
            let affichage;
            if (estPlatChoisi) {
                affichage = "flex";
            } else {
                affichage = "none";
            }
            article.style.display = affichage;
            if (StockEpuise(article)) {
                article.style.opacity = "0.5";
                article.style.pointerEvents = "none";
                article.style.filter = "grayscale(100%)";
            }
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
    const lstArticles = Array.from(container.querySelectorAll(".deux"));
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
    const lstArticles = Array.from(container.querySelectorAll(".deux"));
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
    const articles = document.querySelectorAll(".deux");
    articles.forEach(article => {
        article.style.display = "flex";
        if (StockEpuise(article)) {
            article.style.opacity = "0.5";
            article.style.pointerEvents = "none";
            article.style.filter = "grayscale(100%)";
        }
    });
    btnPlat.forEach(b => {
        b.style.backgroundColor = "";
        b.querySelector("p").style.borderBottom = "";
    });
});


function effectuerRecherche() {
    let valRecherche = document.getElementById("recherche_bare").value.toLowerCase();
    const articles = document.querySelectorAll(".deux");
    articles.forEach(article => {
        const nomPlat = article.querySelector("h5").textContent.toLowerCase();
        const idTp = article.dataset.idTp;
        let estSelectionne = true;
        if (typePlatChoisi !== null) {
            if (typePlatChoisi === "formules") {
                estSelectionne = article.classList.contains("formule_article");
            } else {
                estSelectionne = (parseInt(idTp, 10) === typePlatChoisi);
            }
        }
        let affichage;
        if (estSelectionne && nomPlat.includes(valRecherche)) {
            affichage = "flex";
        } else {
            affichage = "none";
        }
        article.style.display = affichage;
        if (StockEpuise(article)) {
            article.style.opacity = "0.5";
            article.style.pointerEvents = "none";
            article.style.filter = "grayscale(100%)";
        }
    })
}

const btnRechercher = document.getElementById("recherche_bouton");
const inputRecherche = document.getElementById("recherche_bare");

btnRechercher.addEventListener("click", (e) => {
    e.preventDefault();
    effectuerRecherche();
    inputRecherche.blur();
});

inputRecherche.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        effectuerRecherche();
        inputRecherche.blur();
    }
});

inputRecherche.addEventListener("input", () => {
    effectuerRecherche();
});

inputRecherche.addEventListener("blur", () => {
    inputRecherche.value = "";
});