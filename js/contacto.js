window.addEventListener("DOMContentLoaded", function () {
    document.getElementById("formulario").addEventListener("submit", function (event) {
        event.preventDefault();
        enviarFormulario();
    });
});

var nombre = document.getElementById("nombre");
var email = document.getElementById("email");
var mensaje = document.getElementById("mensaje");
var errorNombre = document.getElementById("errorNombre");
var errorEmail = document.getElementById("errorEmail");
var errorMensaje = document.getElementById("errorMensaje");

errorNombre.style.color = "red";
errorEmail.style.color = "red";
errorMensaje.style.color = "red";

function enviarFormulario() {

    console.log("enviando formulario");

    var mensajesError = [];

    if (nombre.value === null || nombre.value === "") {
        mensajesError.push("ingresa tu nombre");
    }

    if (email.value === null || email.value === "") {
        mensajesError.push("ingresa tu correo electronico");
    }

    if (mensaje.value === null || mensaje.value === "") {
        mensajesError.push("Dejanos tu mensaje");
    }

    errorNombre.innerHTML = mensajesError.find((mensaje) => mensaje.includes("nombre")) || "";
    errorEmail.innerHTML = mensajesError.find((mensaje) => mensaje.includes("correo")) || "";
    errorMensaje.innerHTML = mensajesError.find((mensaje) => mensaje.includes("mensaje")) || "";

    if (mensajesError.length === 0 || mensajesError === null) {
        var myModalEl = document.querySelector('#staticBackdrop');
        var modal = bootstrap.Modal.getOrCreateInstance(myModalEl);
        modal.show();

    }



}

