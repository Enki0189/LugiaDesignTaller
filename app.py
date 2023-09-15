from flask import Flask, render_template
from flask import Flask, request
from flask_mysqldb import MySQL
from flask import Flask, flash, render_template, request, redirect, url_for
from flask import session

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
    cur.execute("SELECT NombreProducto, Descripcion, precio, stock, urlImagen FROM Productos")
    
    # Obtiene todos los resultados de la consulta
    db_products = cur.fetchall()

    # Construye la lista de productos basándonos en los resultados
    products = []
    for product in db_products:
        product_data = {
            "name": product[0],
            "descripcion": product[1], 
            "imagen": product[4], 
            "price": "${:,.2f}".format(product[2]) 
        }
        products.append(product_data)
    return render_template('productos.html', products=products)

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

@app.route('/carrito')
def carrito():
    return render_template("carrito.html")


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

#prueba de flask, no es necesario por ahora
#user profile
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)


#no borrar por ahora
if __name__ == '__main__':
    app.run(port = 3000, debug = True)