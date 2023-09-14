from flask import Flask, render_template
from flask import Flask, request
from flask_mysqldb import MySQL

#flask instance
app = Flask(__name__)

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
@app.route('/producto.html')
def producto():
    return render_template("producto.html")

@app.route('/pagUsuario.html')
def pagUsuario():
    return render_template("pagUsuario.html")

@app.route('/login.html')
def login():
    return render_template("login.html")

@app.route('/register.html')
def register():
    return render_template("register.html")

@app.route('/carrito.html')
def carrito():
    return render_template("carrito.html")


@app.route('/usuario' , methods = ['POST'])
def crearUsuario():
    print('Se recibe solicitud de creacion de nuevo usuario.')
    id = 3
    nombreUsuario = request.form['userName']
    password = request.form['password']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    telefono = request.form['phone']
    direccion = request.form['address']
    provincia = request.form['province']
    personalId = request.form['personalId']
    nombreYapellido = nombre + ' ' + apellido
    rol = 1
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO usuario (idUsuario, nombreUsuario, contraseña, rol, email, direccion, telefono, nombreYapellido, cuil, provincia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (id, nombreUsuario, password, rol, email, direccion, telefono, nombreYapellido, personalId, provincia))
    mysql.connection.commit()

#prueba de flask, no es necesario por ahora
#user profile
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)


#no borrar por ahora
if __name__ == '__main__':
    app.run(port = 3000, debug = True)