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