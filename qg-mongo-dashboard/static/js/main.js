$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

function mongoCurrentOp(name) {
    console.log(name);
}