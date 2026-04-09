from flask import Blueprint
from aplicacion.utilidades.seguridad import login_requerido, requiere_modulo

finanzas_bp = Blueprint('finanzas', __name__)

@finanzas_bp.route("/finanzas")
@login_requerido
@requiere_modulo("finanzas")
def inicio():
    return "<h1>Módulo de Mantenimiento en construcción</h1><a href='/panel'>Volver</a>"