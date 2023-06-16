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