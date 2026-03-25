from flask import Flask, redirect,render_template
from aplicacion.rutas.autenticacion.rutas import autenticacion_bp
from dotenv import load_dotenv
from aplicacion.extensiones.base_datos import obtener_sesion
from aplicacion.modelos.erp.articulos import Articulo
import aplicacion.modelos
from aplicacion.utilidades.seguridad import login_requerido
import os

load_dotenv()

app = Flask(__name__, template_folder="aplicacion/templates", static_folder="aplicacion/static")
app.secret_key = os.getenv("CLAVE_SECRETA")

app.register_blueprint(autenticacion_bp)

@app.route("/")
def inicio():
    return redirect("/login")

@app.route("/panel")
@login_requerido
def panel():

    return render_template("panel/panel.html", mostrar_sidebar=True)

@app.route("/inventario")
@login_requerido
def inventario():
    sesion = obtener_sesion()
    productos = sesion.query(Articulo).all()
    sesion.close()
    return render_template("inventario/inventario.html" , productos=productos, mostrar_sidebar=True)

if __name__ == "__main__":
    app.run(debug=True)