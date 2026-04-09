from flask import Blueprint, render_template, request, redirect, url_for, session
from aplicacion.rutas.autenticacion.rutas import autenticacion_bp
from dotenv import load_dotenv
from aplicacion.servicios.servicio_inventario import obtener_inventario
from aplicacion.modelos.erp.articulos import Articulo
from aplicacion.utilidades.seguridad import login_requerido
from aplicacion.servicios.servicio_autenticacion import verificar_configuracion
from aplicacion.utilidades.modulos import requiere_modulo
from aplicacion.servicios.servicio_inventario import registrar_articulo, articulo_lote, obtener_articulo
from aplicacion.modelos.erp.lotes import LoteInventario 


inventario_bp = Blueprint('inventario', __name__)


@inventario_bp.route("/inventario")
@login_requerido
@requiere_modulo("inventario")
def inventario():
    productos=obtener_inventario()
    return render_template("inventario/inventario.html" , productos=productos, mostrar_sidebar=True)


@inventario_bp.route("/Nuevo_producto", methods=["GET", "POST"])
@login_requerido
@requiere_modulo("inventario")
def nuevo_producto():
    if request.method == "POST":
        exito = registrar_articulo(request.form)

        if exito:
            return redirect(url_for('inventario.inventario'))
        else:
            return "Ocurrió un error al guardar el producto", 500
    return render_template("inventario/agregar_producto.html", mostrar_sidebar=True)



@inventario_bp.route("/inventario/surtir/<int:id>", methods=["GET", "POST"])
@login_requerido
@requiere_modulo("inventario")
def surtir_producto(id):
    articulo=obtener_articulo(id)
    if request.method == "POST":
        cantidad_nueva = float(request.form.get("cantidad", 0))
        articulo_lote(id,cantidad_nueva)
        return redirect(url_for('inventario.inventario')) 

    
    return render_template("inventario/surtir.html", articulo=articulo, mostrar_sidebar=True)


