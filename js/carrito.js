let carrito = []; 

function agregarAlCarrito(nombre, precio) {
    // Crea un objeto con los datos del producto
    const producto = {
        nombre: nombre,
        precio: precio
    };
    // Agrega el producto al carrito
    carrito.push(producto);

    actualizarCarrito();
    actualizarContadorCarrito();

    // Realiza una solicitud AJAX para agregar el producto al carrito
    fetch('/agregar-producto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(producto)
    })
    .then(response => response.json())
    .then(data => {
        // Si la solicitud se completó con éxito, actualiza el contador del carrito
        actualizarContadorCarrito();
    })
    .catch(error => {
        console.error('Error al agregar el producto al carrito:', error);
    });
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

document.getElementById('finalizarCompraBtn').addEventListener('click', () => {
    fetch('/iniciar-pago', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ carrito })
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = data.init_point;
    })
    .catch(error => {
        console.error('Error al iniciar el pago:', error);
    });
});
