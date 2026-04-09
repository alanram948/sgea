from flask import Blueprint, render_template, request, redirect, url_for, session
from aplicacion.utilidades.modulos import requiere_modulo
from aplicacion.modelos.erp.articulos import Articulo
import aplicacion.modelos
from aplicacion.utilidades.seguridad import login_requerido
from aplicacion.servicios.servicio_autenticacion import verificar_configuracion
import os
from aplicacion.utilidades.modulos import requiere_modulo

produccion_bp = Blueprint('produccion', __name__)
@produccion_bp.route("/produccion")
@login_requerido
@requiere_modulo("produccion")
def produccion():
    return render_template("produccion.html")