document.getElementById("searchBox").addEventListener("keyup", function() {
    var filter = this.value.toLowerCase();
    var rows = document.getElementById("bookTable").getElementsByTagName("tr");
    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        var found = false;
        for (var j = 0; j < cells.length - 1; j++) { // last cell is actions
            if (cells[j].innerText.toLowerCase().includes(filter)) {
                found = true;
                break;
            }
        }
        rows[i].style.display = found ? "" : "none";
    }
});