const checkoutProduct = document.getElementById("checkout-product");
const checkoutSubtotal = document.getElementById("checkout-subtotal");
const checkoutTotal = document.getElementById("checkout-total");

// consulta si localstorage contiene un carrito.
const carritoPagar = localStorage.getItem("carrito") ? JSON.parse(localStorage.getItem("carrito")) : [];

const subtotal = carritoPagar.reduce((acumulador, x) => acumulador + (x.cantidad * x.precio), 0);

const llenarCard = () => {

    let tablas = ` <tr class="checkout_table-fila">
                        <th class="t2">Producto</th>
                        <th class="t2">Nombre</th>
                        <th class="ps-6">Precio</th>
                </tr>`;
    carritoPagar.forEach(producto => {

        tablas += ` <tr class="checkout_table-fila">
                                        <td><img class="product-img" src="./img/${producto.img}" alt="nb"></td>
                                        <td>${producto.marca}${producto.modelo} x ${producto.cantidad}</td>
                                        <td>$${producto.precio*producto.cantidad}</td>
                                    </tr>
                                    `
    });
    checkoutProduct.innerHTML = tablas;
}

checkoutSubtotal.innerText = "$" + subtotal;
checkoutTotal.innerText = "$" + subtotal;

llenarCard();