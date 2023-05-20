// Datos de ejemplo de productos

const productos  = [
    { id: 1, nombre: 'Producto 1', precio: 10.99 },
    { id: 2, nombre: 'Producto 2', precio: 20.99 },
    { id: 3, nombre: 'Producto 3', precio: 15.99 }
];

// Función para mostrar la lista de productos
function mostrarProductos() {
    const lista = document.getElementById('productos-lista');

    productos.forEach(producto => {
        const li = document.createElement('li');
        li.innerHTML = `<a href="producto.html?id=${producto.id}">${producto.nombre}</a> - $${producto.precio}`;
        lista.appendChild(li);
    });
}

// Mostrar la lista de productos cando la página haya cargado 
window.addEventListener('load', mostrarProductos);

