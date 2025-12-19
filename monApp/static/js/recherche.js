function filtrerTableau() {

    var input = document.getElementById("recherche");
    var filter = input.value.toUpperCase();
    var tbody = document.getElementById("tableBody");
    var tr = tbody.getElementsByTagName("tr");

    for (var i = 0; i < tr.length; i++) {
        var td = tr[i].getElementsByTagName("td")[0]; // On cherche dans la 1ère colonne

        if (td) {
            var txtValue = td.textContent || td.innerText;

            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}