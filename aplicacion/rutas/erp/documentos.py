from flask import Blueprint, render_template, request, redirect, url_for, session, request, jsonify
from aplicacion.servicios.servicio_autenticacion import validar_usuario, registrar_usuario, marcar_configuracion_completa
from aplicacion.servicios.servicio_autenticacion import buscar_lider
from aplicacion.servicios.servicio_ia import bd_ia
from aplicacion.utilidades.seguridad import login_requerido
from aplicacion.utilidades.modulos import requiere_modulo
from aplicacion.servicios.servicio_inventario import obtener_inventario
from aplicacion.servicios.servicio_ventas import venta


erp_bp = Blueprint('erp', __name__)
@erp_bp.route("/ventas")
@login_requerido
@requiere_modulo("ventas")
def ventas():
    
    config = session.get("modulos", {})
    usuario_rol = session.get("rol")
    productos=obtener_inventario()
    return render_template("erp/ventas.html", productos=productos, mostrar_sidebar=True)

@erp_bp.route("/ventas/procesar", methods=["POST"])
@login_requerido
@requiere_modulo("ventas")
def procesar_venta():
    datos = request.get_json()
    usuario_id = session.get("usuario_id")
    carrito = datos.get("items", [])
    
    if not carrito:
        return jsonify({"exito": False, "error": "Carrito vacío"}), 400
    resultado, status_code = venta(datos, usuario_id)
    return jsonify(resultado), status_code