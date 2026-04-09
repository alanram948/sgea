from flask import session, redirect
from functools import wraps

def requiere_modulo(nombre_modulo):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            modulos = session.get("modulos", {})

            if not modulos.get(nombre_modulo):
                return "Módulo no disponible"

            return func(*args, **kwargs)

        return wrapper
    return decorador