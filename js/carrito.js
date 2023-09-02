// carrito.js
let carrito = []; // Almacenar productos en el carrito

function agregarAlCarrito(nombre, precio) {
    const producto = { nombre, precio };
    carrito.push(producto);
    actualizarCarrito();
    actualizarContadorCarrito();
}

function actualizarCarrito() {
    const carritoLista = document.getElementById('carritoLista');
    const totalElement = document.getElementById('total');
    let carritoHTML = '';
    let total = 0;

    carrito.forEach((producto) => {
        carritoHTML += `<li>${producto.nombre}: $${producto.precio}</li>`;
        total += producto.precio;
    });

    carritoLista.innerHTML = carritoHTML;
    totalElement.textContent = total;
}
