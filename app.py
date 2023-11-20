from flask import Flask, render_template
from flask import Flask, request
from flask_mysqldb import MySQL
from flask import Flask, flash, render_template, request, redirect, url_for
from flask import session

# SDK de Mercado Pago
import mercadopago
# Agrega credenciales
sdk = mercadopago.SDK("APP_USR-2668653040880546-091716-bbcb8f8503c6715854fdc44f002834f9-1482234495")


#flask instance
app = Flask(__name__)
app.secret_key = 'alguna_clave_secreta_y_dificil_de_adivinar'

#configuracion base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = '010420'


app.config['MYSQL_DB'] = 'lugia_design'

mysql = MySQL(app)

#create route decorator
@app.route('/')
def index():
    return render_template("index.html")

''' este es el método que intenté usar para la conexión con Node
@app.route('/flask', methods=['GET'])
def flaskServer():
    return "flask server"'''

@app.route('/contacto')
def contacto():
    return render_template("contacto.html")

@app.route('/nosotros')
def nosotros():
    return render_template("nosotros.html")

@app.route('/productos')
def productos():
    cur = mysql.connection.cursor()
    # Ejecuta consulta SQL para obtener productos
    cur.execute("SELECT NombreProducto, Descripcion, precio, stock, urlImagen, idProductos FROM Productos")
    
    # Obtiene todos los resultados de la consulta
    db_products = cur.fetchall()

    # Construye la lista de productos basándonos en los resultados
    products = []
    for product in db_products:
        product_data = {
            "name": product[0],
            "descripcion": product[1], 
            "imagen": product[4], 
            "price": "${:,.2f}".format(product[2]),
            "id": product[5]
        }
        products.append(product_data)
    print("Creando carro vacio")
    if "cart" not in session :
        session["cart"] = []
    print(session["cart"])
    if "totalprice" not in session :
        session["totalprice"] = 0
    session["productosCargados"] = products    
    return render_template('productos.html', products=products)

@app.route('/add_to_cart', methods=["POST"])
def add_to_cart():
    itemId = int(request.form["id"])
    print(session["productosCargados"][itemId-1])
    session["cart"].append(session["productosCargados"][itemId-1])

    productPrice = session["productosCargados"][itemId-1]["price"].replace('$','').replace(',', '')
    session["totalprice"] = float(session["totalprice"]) + float(productPrice)


    print(session["totalprice"])
    print(session["cart"])
    return redirect(url_for('productos'))


@app.route('/carrito')
def carrito():
    productos_carrito = []
    if session["cart"] != []:
        print("hay algo")
        for product in session["cart"]:
            producto_carrito = {
                "nombre": product["name"],
                "precio_unit": product["price"],
                "id": product["id"]
            }
            productos_carrito.append(producto_carrito)        
    else:
        print("vacio")
    print(productos_carrito)
    return render_template("carrito.html")

@app.route('/empty_cart')
def empty_cart():
    session["cart"] = []
    session["totalprice"] = 0
    return render_template("carrito.html")

#producto individual
@app.route('/producto')
def producto():
    return render_template("producto.html")

@app.route('/pagUsuario')
def pagUsuario():
    return render_template("pagUsuario.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/products_mp')
def products_mp():
    return render_template("products_mp.html")


@app.route('/usuario' , methods = ['POST'])
def crearUsuario():
    print('Se recibe solicitud de creacion de nuevo usuario.')
    nombreUsuario = request.form['userName']
    password = request.form['password']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    telefono = request.form['phone']
    direccion = request.form['address']
    provincia = request.form['province']
    nombreYapellido = nombre + ' ' + apellido
    personalId = request.form['personalId']
    rol = 1
    
    try:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuario (nombreUsuario, contraseña, rol, email, direccion, telefono, nombreYapellido, cuil, provincia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (nombreUsuario, password, rol, email, direccion, telefono, nombreYapellido, personalId, provincia))
        mysql.connection.commit()
        flash('Usuario creado exitosamente!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        mysql.connection.rollback()
        print(f"Error: {e}")
        flash('Hubo un error al crear el usuario. Por favor intenta nuevamente.', 'danger')

    return redirect(url_for('register'))

@app.route('/usuario/login' , methods = ['POST'])
def usuarioLogin():
    email = request.form['email']
    password = request.form['password']

    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT email, contraseña FROM usuario WHERE email = %s', [email])
        user = cur.fetchone()
        if user and user[1] == password:  # Aquí simplemente se compara directamente, pero deberías usar hashing.
            session['logged_in'] = True
            session['user_email'] = email
            flash('Inicio de sesión correcto.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario y/o contraseñas incorrectos. Por favor intenta nuevamente.', 'danger')
    except Exception as e:
        print(f"Error: {e}")
        flash('Hubo un error al intentar iniciar sesión. Por favor intenta nuevamente.', 'danger')
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_email', None)
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('index'))


@app.route('/generar')
def payment(req):
    # Crea un ítem en la preferencia
    preference_data = {
        "items": [
            {
                #esto es de prueba, más adelante tomar info de BD
                "title": "Escritorio",
                "description": "escritorio gamer",
                "unit_price": 100,
                "currency_id": "ARS",
                "quantity": 1,
            }
        ]
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

#prueba de flask, no es necesario por ahora
#user profile
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)


#no borrar por ahora
if __name__ == '__main__':
    app.run(port = 3000, debug = True)