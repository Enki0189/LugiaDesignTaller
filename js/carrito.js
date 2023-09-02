// carrito.js

let carrito = []; // Almacenar productos en el carrito

function agregarAlCarrito(nombre, precio) {
    // Buscar si el producto ya está en el carrito
    const productoEnCarrito = carrito.find((item) => item.nombre === nombre);

    if (productoEnCarrito) {
        // Si ya existe, incrementar la cantidad
        productoEnCarrito.cantidad++;
    } else {
        // Si no existe, agregarlo al carrito
        carrito.push({ nombre, precio, cantidad: 1 });
    }

    actualizarCarrito();
    // Llama a esta función para inicializar el contador en cada página
    actualizarContadorCarrito();
}

function actualizarCarrito() {
    const carritoLista = document.getElementById('carritoLista');
    const totalElement = document.getElementById('total');
    let carritoHTML = '';
    let total = 0;

    carrito.forEach((producto) => {
        carritoHTML += `<li>${producto.nombre} x ${producto.cantidad}: $${producto.precio * producto.cantidad}</li>`;
        total += producto.precio * producto.cantidad;
    });

    carritoLista.innerHTML = carritoHTML;
    totalElement.textContent = total;
}

function actualizarContadorCarrito() {
    const carritoContador = document.getElementById('carritoContador');
    carritoContador.textContent = carrito.length;
}

document.getElementById('finalizarCompra').addEventListener('click', () => {
    // Enviar los datos del carrito al servidor para iniciar el proceso de pago
    fetch('/iniciar-pago', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ carrito })
    })
    .then(response => response.json())
    .then(data => {
        // Redirigir al usuario a la URL de MercadoPago para completar el pago
        window.location.href = data.init_point;
    })
    .catch(error => {
        console.error('Error al iniciar el pago:', error);
    });
});

// Función para eliminar un producto del carrito (opcional)
function eliminarDelCarrito(nombre) {
    const index = carrito.findIndex((item) => item.nombre === nombre);
    if (index !== -1) {
        carrito.splice(index, 1);
        actualizarCarrito();
    }
}

// Puedes agregar más funciones relacionadas con el carrito según tus necesidades
