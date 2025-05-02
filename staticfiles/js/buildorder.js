document.getElementById("myDropdown").addEventListener("change", function() {
    var selectedOption = this.value;
    var dropdownContent = document.getElementById("dropdownContent");

    // Hide all content sections
    dropdownContent.querySelectorAll("p").forEach(function(p) {
        p.style.display = "none";
    });

    // Show the content section corresponding to the selected option
    document.getElementById(selectedOption + "Content").style.display = "block";
    console.log("hello world");
});