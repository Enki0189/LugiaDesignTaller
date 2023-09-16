from flask import Flask, render_template

#flask instance
app = Flask(__name__)

#create route decorator
@app.route('/')

def index():
    return render_template("index.html")

@app.route('/contacto.html')
def contacto():
    return render_template("contacto.html")

@app.route('/nosotros.html')
def nosotros():
    return render_template("nosotros.html")

#todos los productos
@app.route('/productos.html')
def productos():
    return render_template("productos.html")

#producto individual
@app.route('/producto.html')
def producto():
    return render_template("producto.html")

@app.route('/pagUsuario.html')
def pagUsuario():
    return render_template("pagUsuario.html")


#prueba de flask, no es necesario por ahora
#user profile
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)


#no borrar por ahora
if __name__ == '__main__':
    app.run(port = 3000, debug = True)

#-----------.............-----------carrito -------------...............-----------------------

from flask import Flask, render_template, request, jsonify
import mercadopago

app = Flask(__name__)

# Configura tu token de acceso de MercadoPago
ACCESS_TOKEN = 'TEST-6306101317624376-060219-a45c93a10a3aef2fcf5a3df0561fe9d3-207146047'

sdk = mercadopago.SDK(ACCESS_TOKEN)

# Lista de productos (para simular el carrito)
productos = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iniciar-pago', methods=['POST'])
def iniciar_pago():
    global productos

    # Recibe los datos del carrito desde la solicitud AJAX
    carrito_data = request.get_json()

    # Prepara los datos del pago para MercadoPago
    payment_data = {
        "transaction_amount": calcular_total_carrito(productos),  # Implementa esta función
        "token": "CARD_TOKEN",  # Debes obtener el token de la tarjeta de algún lugar
        "description": "Descripción del pago",
        "payment_method_id": 'visa',
        "installments": 1,
        "payer": {
            "email": 'test_user_123456@testuser.com'
        }
    }

    # Crea el pago en MercadoPago
    result = sdk.payment().create(payment_data)
    payment = result["response"]

    # Limpia el carrito después de completar el pago
    productos = []

    return jsonify({"init_point": payment['transaction_details']['external_resource_url']})

@app.route('/agregar-producto', methods=['POST'])
def agregar_producto():
    global productos

    # Recibe los datos del producto desde la solicitud AJAX
    producto_data = request.get_json()

    # Agrega el producto al carrito
    productos.append(producto_data)

    return jsonify({"message": "Producto agregado al carrito"})

if __name__ == '__main__':
    app.run(debug=True)
