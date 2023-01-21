console.log('esta linkado')

document.addEventListener('DOMContentLoaded', () => {
    var header = document.getElementById("navi"); // pego a minha navbar
    var btns = header.getElementsByClassName("nav-link"); // pego os meus botoes
    for (var i = 0; i < btns.length; i++)
    {
        btns[i].addEventListener("click", function() {
        var current = document.getElementsByClassName("active");
        current[0].className = current[0].className.replace(" active", "");
        this.className += " active";
        if (this.id == "Classwork")
        {
            document.getElementById("heading-description").classList.add("apagado");
            document.getElementById("desc-description").classList.add("apagado");
            document.getElementById("heading-students").classList.remove("apagado");
            document.getElementById("desc-students").classList.remove("apagado");
        }
        else if (this.id == "Stream")
        {
            document.getElementById("heading-description").classList.remove("apagado");
            document.getElementById("desc-description").classList.remove("apagado");
            document.getElementById("heading-students").classList.add("apagado");
            document.getElementById("desc-students").classList.add("apagado");
        }
    });
  }
});

