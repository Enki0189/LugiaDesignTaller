from flask import Flask, render_template, request
from flask import Flask, render_template, request
import mercadopago

app = Flask(__name__)

# SDK de Mercado Pago
sdk = mercadopago.SDK("
# SDK de Mercado Pago
import mercadopago
# Agrega credenciales
sdk = mercadopago.SDK("PROD_ACCESS_TOKEN")
")


# Datos de ejemplo de productos
productos = [
    { 'id': 1, 'nombre': 'Producto 1', 'precio': 10.99 },
    { 'id': 2, 'nombre': 'Producto 2', 'precio': 20.99 },
    { 'id': 3, 'nombre': 'Producto 3', 'precio': 15.99 }
]

@app.route('/')
def listar_productos():
    return render_template('productos.html', productos=productos)

@app.route('/producto/<int:id>')
def mostrar_producto(id):
    producto = next((p for p in productos if p['id'] == id), None)
    if producto:
        return render_template('producto.html', producto=producto)
    else:
        return 'Producto no encontrado.'

if __name__ == '__main__':
    app.run()

@app.route('/carrito', methods=['POST'])
def agregar_al_carrito():
    producto_id = request.form['producto_id']
    producto = next((p for p in productos if str(p['id']) == producto_id), None)
    if producto:
        preference_data = {
            "items": [
                {
                    "title": producto['nombre'],
                    "quantity": 1,
                    "currency_id": "ARS",
                    "unit_price": producto['precio']
                }
            ]
        }
        preference = mp.preference().create(preference_data)
        return render_template('carrito.html', preference_id=preference['id'])
    else:
        return 'Producto no encontrado.'
