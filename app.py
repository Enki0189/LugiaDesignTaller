from flask import Flask, render_template
from flask import Flask, request
from flask_mysqldb import MySQL
from flask import Flask, flash, render_template, request, redirect, url_for
from flask import session

# SDK de Mercado Pago
import mercadopago
# Agrega access token de aplicacion de mercado pago
sdk = mercadopago.SDK("TEST-2662247305576876-112118-aef012964bf37797f2668f83221e4db7-418530695")


#flask instance
app = Flask(__name__)
app.secret_key = 'alguna_clave_secreta_y_dificil_de_adivinar'

#configuracion base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '6277Horde' #'010420'
app.config['MYSQL_DB'] = 'lugia_design'

mysql = MySQL(app)

#create route decorator
@app.route('/')
def index():
    return render_template("index.html")

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
            "quantity": 0,
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
    print(itemId)

    # Buscar el producto en session["productosCargados"] usando una función lambda
    selected_product = next((product for product in session["productosCargados"] if product["id"] == itemId), None)

    if selected_product:
        # Buscar el producto en session["cart"] usando una función lambda
        cart_product = next((product for product in session["cart"] if product["id"] == itemId), None)

        if cart_product:
            # Incrementar la propiedad "quantity" en 1 si ya existe en el carrito
            cart_product["quantity"] += 1
        else:
            # Agregar el producto al carrito con "quantity" establecido en 1
            selected_product["quantity"] = 1
            session["cart"].append(selected_product)

        productPrice = selected_product["price"].replace('$', '').replace(',', '')
        session["totalprice"] = float(session["totalprice"]) + float(productPrice)

    return redirect(url_for('productos'))



@app.route('/empty_cart')
def empty_cart():
    session["cart"] = []
    session["totalprice"] = 0
    flash('Se han eliminado todos los productos del carrito', 'success')
    return redirect(url_for("productos"))


@app.route('/pagUsuario')
def pagUsuario():
    cur = mysql.connection.cursor()
    cur.execute("SELECT NombreUsuario, Contraseña, Rol, Email, Direccion, Telefono, nombreYapellido, cuil, provincia FROM usuario")
    info_users = cur.fetchall()
    usuario_actual = []
    if "current_user" not in session:
        session["current_user"] = []
    #print(info_users)
    for user in info_users:
        if user[3] == session['user_email']:
            current_user = {
                "user": user[0],
                "name": user[6],
                "email": user[3],
                "cuil": user[7],
                "phone": user[5],
                "province": user[8],
                "address": user[4],
                "password": user[1],
                "role": user[2]
            }
            usuario_actual.append(current_user)
            
    session["current_user"] = usuario_actual
    print(session["current_user"])
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

@app.route('/abmProducto')
def abmProducto():
    return render_template("abmProducto.html")

@app.route('/producto' , methods = ['POST'])
def crearProducto():
    print('Se recibe solicitud de creacion de nuevo producto.')
    nombreProducto = request.form['nombreProducto']
    urlImagen = request.form['urlImagen']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    stock = request.form['stock']
    
    try:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (nombreProducto, descripcion, precio, stock, urlImagen) VALUES (%s, %s, %s, %s, %s)', (nombreProducto, descripcion, precio, stock, urlImagen))
        mysql.connection.commit()
        flash('Producto creado exitosamente!', 'success')
        return redirect(url_for('productos'))
    except Exception as e:
        mysql.connection.rollback()
        print(f"Error: {e}")
        flash('Hubo un error al crear el producto. Por favor intenta nuevamente.', 'danger')

    return redirect(url_for('abmProducto'))


@app.route('/producto/<int:idProducto>' , methods = ['PUT'])
def editarProducto(idProducto):
    print('Se recibe edicion de producto.')
    nombreProducto = request.form['nombreProducto']
    urlImagen = request.form['urlImagen']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    stock = request.form['stock']
    
    try:
        cur = mysql.connection.cursor()
        cur.execute('UPDATE productos SET nombreProducto = %s, descripcion = %s, precio = %s, stock = %s, urlImagen = %s WHERE idProductos = %s', (nombreProducto, descripcion, precio, stock, urlImagen, idProducto))
        mysql.connection.commit()
        flash('Producto actualizado exitosamente!', 'success')
        return redirect(url_for('productos'))
    except Exception as e:
        mysql.connection.rollback()
        print(f"Error: {e}")
        flash('Hubo un error al actualizar el producto. Por favor intenta nuevamente.', 'danger')

    return redirect(url_for('abmProducto'))

@app.route('/producto/<int:idProducto>' , methods = ['DELETE'])
def borrarProducto(idProducto):
    print('Se recibe eliminacion de producto.')
    
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM productos WHERE idProductos = ' + str(idProducto))
        mysql.connection.commit()
        flash('Producto eliminado exitosamente!', 'success')
        return redirect(url_for('productos'))
    except Exception as e:
        mysql.connection.rollback()
        print(f"Error: {e}")
        flash('Hubo un error al eliminar el producto. Por favor intenta nuevamente.', 'danger')

    return redirect(url_for('productos'))

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
        cur.execute('SELECT U.email, U.contraseña, R.descripcion FROM usuario U JOIN roles R ON U.rol = R.idRoles WHERE email = %s', [email])
        user = cur.fetchone()
        if user and user[1] == password:  # Aquí simplemente se compara directamente, pero deberíamos usar hashing.
            session['logged_in'] = True
            session['user_email'] = email
            session['tipo_usuario'] = user[2]
            flash('Inicio de sesión correcto.', 'success')
            return redirect(url_for('index'))
        else:
            flash('E-mail y/o contraseña incorrectos. Por favor intenta nuevamente.', 'danger')
    except Exception as e:
        print(f"Error: {e}")
        flash('Hubo un error al intentar iniciar sesión. Por favor intenta nuevamente.', 'danger')
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_email', None)
    session.pop('tipo_usuario', None)
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('login'))

@app.route('/checkout', methods=['POST'])
def checkout():    
    items = []
    print(f'Sesion cart: {session["cart"]}')
    for product in session["cart"]:
            items.append({
                "title": product["name"],
                "description": product["descripcion"],
                "unit_price": float(product["price"].replace('$','').replace(',', '')),
                "currency_id": "ARS",
                "quantity": product["quantity"],
            })
    print(f"Items: {items}")

    preference_data = {
        "items": items,
        "payer": {
            "name": "João",
            "surname": "Silva",
            "email": "user@email.com",
            "phone": {
                "area_code": "11",
                "number": "4444-4444"
            },
            "identification": {
                "type": "CPF",
                "number": "19119119100"
            },
            "address": {
                "street_name": "Street",
                "street_number": 123,
                "zip_code": "06233200"
            }
        },
        "back_urls": {
            "success": "http://localhost:5000/",
            "failure": "http://localhost:5000/",
            "pending": "http://localhost:5000/productos"
        },
        "auto_return": "approved",
        "payment_methods": {
          "excluded_payment_methods": [],
          "excluded_payment_types": [],
          "installments": 3
        }
    }
    
    reference_response = sdk.preference().create(preference_data)
    preference_id = reference_response['response']['id']
    
    session["preferenceId"] = preference_id
    # Puedes redirigir a otra página después de procesar los datos
    return render_template('mercadoPago.html')


#prueba de flask, no es necesario por ahora
#user profile
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)


#no borrar por ahora
if __name__ == '__main__':
    app.run(port = 3000, debug = True)