// variables 
const form = document.getElementById("form");
const inputs = [...document.querySelectorAll(".form_input")];
const nombre = document.getElementById("nombre");
const surname = document.getElementById("surname");
const email = document.querySelector("#email");
const phone = document.getElementById("phone");
const dni = document.getElementById("dni");
const formError = document.getElementById("form_mensajeError");

// objeto con expreciones regulares para validar datos
const expresiones = {
    nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
    email: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
    phone: /^\d{8,14}$/ // 8 a 14 numeros.
}

// objeto para validar que todos los campos esten correctos.
const campos = {
        nombre: false,
        surname: false,
        email: false,
        phone: false,
        dni: false
    }
    // funcion que retorna bool. Para verificar que todos los campos esten validados.
const checkCampos = () => { return campos.nombre && campos.surname && campos.email && campos.dni && campos.phone };

// agrega class para valor si es correcto o incorrecto. selecciona tag abuelo del input para agregar la clase correspondiente.
const valueWrong = (input) => {
    const padre = input.parentElement.parentElement;
    padre.className = "form_grupo-incorrecto";
}

const valueRight = (input) => {
    const padre = input.parentElement.parentElement;
    padre.className = "form_grupo-correcto";
}

// valida los campos retornando un bool.
const validarCampo = (input, expresion) => {

    if (input.value === "") {
        valueWrong(input);
        return false;
    } else if (!expresion.test(input.value)) {
        valueWrong(input, ``);
        return false;
    } else {
        valueRight(input);
        return true;
    }

}
const validarPhone = () => {

    if (phone.value === "") {
        valueWrong(phone);
        campos.phone = false;
    } else if ((!expresiones.phone.test(phone.value)) || (phone.value.length < 10)) {
        valueWrong(phone);
        campos.phone = false;
    } else {
        valueRight(phone);
        campos.phone = true;
    }
}

// selecciona el input que corresponda y lo valida.
const validarFormulario = (input) => {

    switch (input) {
        case nombre:
            campos.nombre = validarCampo(nombre, expresiones.nombre, campos.nombre);
            break;

        case surname:
            campos.surname = validarCampo(surname, expresiones.nombre, campos.surname);
            break;

        case email:
            campos.email = validarCampo(email, expresiones.email, campos.email);
            break;
        case phone:
            validarPhone();
            break;
        case dni:
            campos.dni = validarCampo(dni, expresiones.phone, campos.dni);
            break;

        default:
            break;
    }
    if (checkCampos()) {
        formError.classList.remove("form_mensajeError-active");
    }

}

// funcion principal. eschucha evento submit, si esta validado el formulario ejecuta para pagar con mp.
checkoutFormulario = () => {
    // Agregar un novalidateatributo al elemento del formulario evita la validación nativa en los elementos del formulario (si se aplica), 
    // lo que permite que JavaScript administre todas las validaciones sin obstrucciones.
    form.noValidate = true;

    form.addEventListener("submit", e => {

        e.preventDefault();

        inputs.forEach(input => {
            validarFormulario(input);
        });

        if (checkCampos()) {
            const loader = document.getElementById("loader");
            loader.classList.remove("loader2");
            setTimeout(() => {
                mercadoPago();
                localStorage.removeItem("carrito");
            }, 3000);
        } else {
            formError.classList.add("form_mensajeError-active");
        }
    })

    inputs.forEach(input => {
        input.addEventListener(`keyup`, () => validarFormulario(input));
        input.addEventListener(`blur`, () => validarFormulario(input));
    });
}

const myLocation = localStorage.getItem("location") ? localStorage.getItem("location") : "";

// consulta api mercadoPago para generar un link de pago
const mercadoPago = async() => {
    const carritoPagarToMap = carritoPagar.map(item => {
        let newItem = {
            title: item.marca,
            description: "",
            picture_url: item.img,
            category_id: item.id,
            quantity: item.cantidad,
            currency_id: "ARS",
            unit_price: item.precio
        }
        return newItem;
    });

    try {
        const response = await fetch("https://api.mercadopago.com/checkout/preferences", {
            method: "POST",
            headers: {
                Authorization: "Bearer TEST-8514425299917286-050222-065f8d498e17e3869b7f50573fdf0e82-109819640"
            },
            body: JSON.stringify({
                items: carritoPagarToMap,
                back_urls: {
                    "success": "http://127.0.0.1:5501/graciascompra.html",
                    "failure": myLocation,
                    "pending": myLocation
                },
                auto_return: "approved"
            })

        });
        const data = await response.json();
        window.open(data.init_point, "_self")
    } catch (error) {
        console.log(error);
    }
}

// Main
checkoutFormulario();