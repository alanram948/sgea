from functools import wraps
from flask import session, redirect

def login_requerido(funcion):
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        if "usuario" not in session:
            return redirect("/login")
        return funcion(*args, **kwargs)
    return envoltura