from flask import Blueprint, render_template, request, redirect, url_for, session
from aplicacion.servicios.servicio_autenticacion import validar_usuario
from aplicacion.servicios.servicio_autenticacion import registrar_usuario


autenticacion_bp = Blueprint('autenticacion', __name__)

@autenticacion_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["usuario"]
        contrasena = request.form["contrasena"]

        usuario = validar_usuario(email, contrasena)

        if usuario:
            session["usuario"] = usuario.nombre_completo
            return redirect("/panel")
        else:
            return "Credenciales incorrectas"

    return render_template("autenticacion/inicio_sesion.html", mostrar_sidebar=False)

@autenticacion_bp.route("/registro", methods=["GET", "POST"])
def registro():
     
     if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        contrasena = request.form["contrasena"]

        exito = registrar_usuario(nombre, email, contrasena)

        if exito:
            return redirect("/login")
        else:
            return ("El usuario ya existe")

     return render_template("autenticacion/registro.html")