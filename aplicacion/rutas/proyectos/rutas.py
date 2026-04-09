from flask import Blueprint
from aplicacion.utilidades.seguridad import login_requerido, requiere_modulo

proyectos_bp = Blueprint('proyectos', __name__)

@proyectos_bp.route("/proyectos")
@login_requerido
@requiere_modulo("proyectos")
def inicio():
    return "<h1>Módulo de Mantenimiento en construcción </h1><a href='/panel'>Volver</a>"