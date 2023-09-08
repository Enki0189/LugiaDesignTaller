// Función para obtener el parámetro "id" de la URL
function obtenerIdProducto() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Función para mostrar los detalles del producto
function mostrarProducto() {
    const id = obtenerIdProducto();
    const producto = productos.find(p => p.id.toString() === id.toString());

    if (producto) {
        const detalles = document.getElementById('producto-detalles');
        detalles.innerHTML = `
        <h2>${producto.nombre}</h2>
        <p>Precio: $${producto.precio}</p>
        `;

        const botonAgregar = document.getElementById('agregar-carrito');
        botonAgregar.addEventListener('click', ( ) => {
            agregarAlCarrito(producto);
        });
    } else {
        detalles.innerHTML = 'Producto no encontrado. ';
    }
  }

  // Función para agregar un producto al carrito
  function agregarAlCarrito(producto) {
    // Logica para agregar el producto al carrito utilizando API de Mercado Pago
    // utilizar la API de Mercado Pago para agregar el producto al carrito
    // https://www.mercadopago.com.ar/
  }