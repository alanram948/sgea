from aplicacion.extensiones.base_datos import obtener_sesion
from aplicacion.modelos.nucleo.usuarios import Usuario, ConfiguracionEmpresa
from aplicacion.modelos.nucleo.areas import Area
from aplicacion.modelos.nucleo.roles import Rol
from werkzeug.security import generate_password_hash, check_password_hash



def validar_usuario(email, contrasena):
    sesion = obtener_sesion()
    try:
        usuario = sesion.query(Usuario).filter_by(email=email).first()
        if usuario and check_password_hash(usuario.password, contrasena):
            rol=sesion.query(Rol).filter(usuario.id_rol==Rol.id_rol).first()
            usuario_data={"Id":usuario.id_usuario, "Rol":rol.nombre_rol}
            
            return usuario_data
        return None
    finally:    
        sesion.close()
    
def obtener_modulos_lider(id):
    sesion_bd = obtener_sesion()
    config = sesion_bd.query(ConfiguracionEmpresa).filter_by(id_usuario=id).first()
    sesion_bd.close()
    return config

def registrar_usuario(nombre, email, contrasena, rol_nombre):
    sesion = obtener_sesion()
    rol = sesion.query(Rol).filter_by(nombre_rol=rol_nombre).first()
    contrasena_hasheada = generate_password_hash(contrasena)
    if not rol:
        rol = Rol(nombre_rol=rol_nombre)
        sesion.add(rol)
        sesion.commit()

    nuevo = Usuario(
        nombre_completo=nombre,
        email=email,
        password=contrasena_hasheada,
        id_rol=rol.id_rol
    )

    sesion.add(nuevo)
    sesion.commit()
    id_usuario=nuevo.id_usuario
    sesion.close()
    return id_usuario


def obtener_catalogos_empleados():
    sesion = obtener_sesion()
    try:
        roles = sesion.query(Rol).all()
        areas = sesion.query(Area).all()
        supervisores = sesion.query(Usuario).all() 
        return roles, areas, supervisores
    finally:
        sesion.close()

def registrar_empleado(datos_formulario):
    
    sesion = obtener_sesion()
    try:
        
        contrasena_hasheada = generate_password_hash(datos_formulario.get("password"))
        
       
        id_supervisor = datos_formulario.get("id_supervisor")
        id_supervisor = int(id_supervisor) if id_supervisor else None

        nuevo_usuario = Usuario(
            nombre_completo=datos_formulario.get("nombre"),
            email=datos_formulario.get("correo"),
            password=contrasena_hasheada,
            fecha_contratacion=datos_formulario.get("fecha_contratacion"),
            salario_mensual=float(datos_formulario.get("salario_mensual", 0)),
            id_rol=int(datos_formulario.get("id_rol")),
            id_area=int(datos_formulario.get("id_area")),
            id_supervisor=id_supervisor,
            completo_configuracion=True 
        )
        
        sesion.add(nuevo_usuario)
        sesion.commit()
        return True
    except Exception as e:
        sesion.rollback()
        print(f"Error al registrar empleado: {e}")
        return False
    finally:
        sesion.close()

def verificar_configuracion(usuario_id):
    
    sesion = obtener_sesion()
    
    usuario = sesion.query(Usuario).get(usuario_id)
    if not usuario:
        sesion.close()
        return False

    configuracion = usuario.completo_configuracion
    
    sesion.close()
    
    return configuracion
    

def marcar_configuracion_completa(usuario_id):
    sesion = obtener_sesion()

    usuario = sesion.query(Usuario).get(usuario_id)
    usuario.completo_configuracion = True

    sesion.commit()
    sesion.close()

def buscar_lider():
    sesion = obtener_sesion()

    lider = sesion.query(Usuario)\
        .join(Rol)\
        .filter(Rol.nombre_rol == "LIDER")\
        .first()

    sesion.close()

    return lider
def obtener_usuario(id_usuario):
    sesion=obtener_sesion()
    return sesion.query(Usuario).filter_by(Usuario.id_usuario==id_usuario).first()