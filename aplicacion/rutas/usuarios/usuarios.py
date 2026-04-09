from flask import Blueprint, render_template, request, redirect, url_for, session
from aplicacion.servicios.servicio_autenticacion import validar_usuario, registrar_empleado, marcar_configuracion_completa, obtener_catalogos_empleados
from aplicacion.servicios.servicio_autenticacion import buscar_lider
from aplicacion.servicios.servicio_ia import bd_ia
from aplicacion.utilidades.seguridad import login_requerido, requiere_lider
from aplicacion.extensiones.base_datos import obtener_sesion
from aplicacion.modelos.nucleo.usuarios import Usuario
from aplicacion.modelos.nucleo.roles import Rol
usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route("/Personal", methods=["GET", "POST"])
@login_requerido
@requiere_lider
def personal():
    sesion=obtener_sesion()
    usuarios_bd=sesion.query(Usuario, Rol).join(Rol, Usuario.id_rol==Rol.id_rol).all()
    sesion.close()
    return render_template("usuarios/personal.html", usuarios_bd=usuarios_bd,  mostrar_sidebar=True)

@usuarios_bp.route("/personal/nuevo", methods=["GET", "POST"])
@login_requerido
@requiere_lider
def nuevo_empleado():
    if request.method == "POST":
        exito = registrar_empleado(request.form)
        if exito:
            
            return redirect(url_for('usuarios.personal')) 
        else:
            return "Error al guardar el empleado", 500

    
    roles, areas, supervisores = obtener_catalogos_empleados()
    
    return render_template(
        "usuarios/usuarios.html", 
        roles=roles, 
        areas=areas, 
        supervisores=supervisores,
        mostrar_sidebar=True
    )