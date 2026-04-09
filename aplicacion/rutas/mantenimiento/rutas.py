from flask import Blueprint
from aplicacion.utilidades.seguridad import login_requerido, requiere_modulo

mantenimiento_bp = Blueprint('mantenimiento', __name__)

@mantenimiento_bp.route("/mantenimiento")
@login_requerido
@requiere_modulo("mantenimiento")
def inicio():
    return "<h1>Módulo de Mantenimiento en construcción 🚧</h1><a href='/panel'>Volver</a>"