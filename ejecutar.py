from flask import Flask, redirect,render_template, session
from aplicacion.rutas.autenticacion.rutas import autenticacion_bp
from aplicacion.rutas.erp.documentos import erp_bp
from aplicacion.rutas.compras.solicitudes import compras_bp
from aplicacion.rutas.mantenimiento.rutas import mantenimiento_bp
from aplicacion.rutas.finanzas.rutas import finanzas_bp
from aplicacion.rutas.proyectos.rutas import proyectos_bp
from aplicacion.rutas.inventario.productos import inventario_bp
from aplicacion.rutas.produccion.produccion import produccion_bp
from aplicacion.rutas.usuarios.usuarios import usuarios_bp
from dotenv import load_dotenv
from aplicacion.modelos.erp.articulos import Articulo
from aplicacion.utilidades.seguridad import login_requerido
from aplicacion.servicios.servicio_autenticacion import verificar_configuracion
from aplicacion.servicios.servicio_erp import obtener_nombre
import os
from aplicacion.servicios.servicio_dashboard import obtener_ventas_semanal
#from pruebas.script_test import inyectar_dummies_paleteria
load_dotenv()
#inyectar_dummies_paleteria()
app = Flask(__name__, template_folder="aplicacion/templates", static_folder="aplicacion/static")
app.secret_key = os.getenv("CLAVE_SECRETA")

app.register_blueprint(autenticacion_bp)
app.register_blueprint(erp_bp)
app.register_blueprint(inventario_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(produccion_bp)
app.register_blueprint(compras_bp)
app.register_blueprint(mantenimiento_bp)
app.register_blueprint(finanzas_bp)
app.register_blueprint(proyectos_bp)

@app.route("/")
def base():
    return redirect("/login")

@app.route("/panel")
@login_requerido
def panel():
    usuario_id = session["usuario_id"]
    check = verificar_configuracion(usuario_id)
    if not check:
        return redirect("/Cuestionario")

    return render_template("panel/panel.html")

@app.route("/inicio")
@login_requerido
def inicio():
    modulos = session.get("modulos", {})
    nombre=obtener_nombre()
    if session.get("rol")=="LIDER":
        metricas=obtener_ventas_semanal()
        return render_template(
            "base.html", 
            mostrar_sidebar=True,
            ventas_hoy=f"{metricas['ventas_hoy']:,.2f}",
            fechas_grafica=metricas['fechas'],
            ventas_grafica=metricas['ventas'],
            tickets_hoy=metricas['tickets_hoy']
        )
    
    return render_template("base.html", nombre=nombre,modulos=modulos, mostrar_sidebar=True)

if __name__ == "__main__":
    app.run(debug=True)

