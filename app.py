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
    print('Se recibe solicitud de creacion de nuevo usuario.')
    password = request.form['password']
    print('password ingresada')
    nombre = request.form['nombre']
    print('nombre ingresado')
    apellido = request.form['apellido']
    print('apellido ingresado')
    email = request.form['email']
    print('email ingresado.')
    telefono = request.form['phone']
    print('telefono ingresado.')
    direccion = request.form['address']
    print('Direccion ingresada.')
    provincia = request.form['province']
    print('Provincia ingresada.')
    personalId = request.form['personalId']
    print('Cuil ingresado')
    nombreYapellido = nombre + ' ' + apellido
    rol = 1
    cur = mysql.connection.cursor()
    print('Dando de alta usuario.')
    cur.execute('INSERT INTO usuario (idUsuario, nombreUsuario, contraseña, rol, email, direccion, telefono, nombreYapellido, cuil, provincia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (id, nombreUsuario, password, rol, email, direccion, telefono, nombreYapellido, personalId, provincia))
    mysql.connection.commit()
    print('Usuario dado de alta.')

#prueba de flask, no es necesario por ahora
#user profile
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)


#no borrar por ahora
if __name__ == '__main__':
    app.run(port = 3000, debug = True)