from functools import wraps
from flask import session, redirect
from aplicacion.servicios.servicio_autenticacion import obtener_usuario

def login_requerido(funcion):
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect("/login")
        return funcion(*args, **kwargs)
    return envoltura

def tiene_modulos(usuario_id):

    usuario = obtener_usuario(usuario_id)

    return usuario.modulos_json is not None

def requiere_lider(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if session.get("rol") != "LIDER":
            return "No autorizado"

        return func(*args, **kwargs)

    return wrapper

def requiere_modulo(modulo):
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            
            modulos_activos = session.get("modulos", {})
            
            
            if not modulos_activos.get(modulo):
                
                
                return redirect("/panel")
            
        
            return f(*args, **kwargs)
        return decorated_function
    return decorator