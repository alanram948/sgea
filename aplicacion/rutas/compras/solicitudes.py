from flask import Blueprint, render_template
from aplicacion.utilidades.seguridad import login_requerido, requiere_modulo

compras_bp = Blueprint('compras', __name__)

@compras_bp.route("/compras")
@login_requerido
@requiere_modulo("compras")
def inicio():
    return "<h1>Módulo de Compras en construcción</h1><a href='/panel'>Volver</a>"