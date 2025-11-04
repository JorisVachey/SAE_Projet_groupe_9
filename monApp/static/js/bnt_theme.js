const toggleButton = document.querySelector('#toggle-theme');
const body = document.body;
const savedTheme = localStorage.theme;
if (savedTheme) {
    body.classList.add(savedTheme);
}
toggleButton.addEventListener("click", () => {
    body.classList.toggle("dark"); // Ajoute ou enlève la classe "dark"
    const theme = body.classList.contains("dark") ? "dark" : "";
    localStorage.theme = theme; // Sauvegarde le thème dans LocalStorage
});
window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (event) => {
    body.classList.remove("dark");
    localStorage.theme = "";
    if (event.matches) {
        body.classList.add("dark");
        localStorage.theme = "dark";
    }
});
console.log("test si code appliquer");