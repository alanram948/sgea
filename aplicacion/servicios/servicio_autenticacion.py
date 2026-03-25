from aplicacion.extensiones.base_datos import obtener_sesion
from aplicacion.modelos.nucleo.usuarios import Usuario

def validar_usuario(email, contrasena):
    sesion = obtener_sesion()

    usuario = sesion.query(Usuario).filter_by(email=email).first()

    if usuario and usuario.password == contrasena:
        sesion.close()
        return usuario
    
    sesion.close()
    return None


def registrar_usuario(nombre, email, contrasena):
    sesion = obtener_sesion()

    # Verificar si ya existe
    existente = sesion.query(Usuario).filter_by(email=email).first()

    if existente:
        sesion.close()
        return False

    nuevo = Usuario(
        nombre_completo=nombre,
        email=email,
        password=contrasena
    )

    sesion.add(nuevo)
    sesion.commit()
    sesion.close()

    return True