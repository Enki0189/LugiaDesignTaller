from flask import Flask, render_template , request , redirect , url_for, jsonify
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

# rutas de usuario

@app.route('/usuario' , methods = ['POST'])
def crearUsuario():
    print('Se recibe solicitud de creacion de nuevo usuario.')
    id = 1
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
    print('Dando de alta usuario.')
    cur.execute('INSERT INTO usuario (idUsuario, nombreUsuario, contraseña, rol, email, direccion, telefono, nombreYapellido, cuil, provincia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (id, nombreUsuario, password, rol, email, direccion, telefono, nombreYapellido, personalId, provincia))
    mysql.connection.commit()
    print('Usuario dado de alta.')

@app.route('/usuario/<int:id>', methods=['DELETE'])
def eliminarUsuario(id):
    try:
        cur = mysql.connection.cursor()

        # Verifica si el usuario existe
        cur.execute("SELECT * FROM usuario WHERE idUsuario = %s", (id,))
        usuario = cur.fetchone()
        if not usuario:
            return "Usuario no encontrado", 404

        # Elimina al usuario
        cur.execute("DELETE FROM usuario WHERE idUsuario = %s", (id,))
        mysql.connection.commit()

        return "Usuario eliminado con éxito", 200

    except Exception as e:
        return f"Error al eliminar el usuario: {str(e)}", 500
    


@app.route('/usuarios', methods=['GET'])
def obtenerUsuarios():
    try:
        cur = mysql.connection.cursor()
        
        # Consulta SQL para obtener todos los usuarios
        cur.execute("SELECT * FROM usuario")
        usuarios = cur.fetchall()
        
        # Convertir el resultado a una lista de diccionarios para JSONificar
        lista_usuarios = []
        for usuario in usuarios:
            lista_usuarios.append({
                'idUsuario': usuario[0],
                'nombreUsuario': usuario[1],
                'contraseña': usuario[2],
                'rol': usuario[3],
                'email': usuario[4],
                'direccion': usuario[5],
                'telefono': usuario[6],
                'nombreYapellido': usuario[7],
                'cuil': usuario[8],
                'provincia': usuario[9]
            })

        # Devolver la lista de usuarios como JSON
        return jsonify(lista_usuarios)

    except Exception as e:
        return f"Error al obtener los usuarios: {str(e)}", 500




#no borrar por ahora
if __name__ == '__main__':
    app.run(port = 3000, debug = True)