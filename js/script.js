const weapon = document.querySelectorAll(".weapon");

weapon.forEach((weap) => {
    weap.addEventListener("click", () => {
        removeActiveClasses();
        weap.classList.add("active");
    });
});

function removeActiveClasses(){
    weapon.forEach((weap) => {
        weap.classList.remove("active");
    });
}