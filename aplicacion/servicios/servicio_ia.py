import joblib
import os
from aplicacion.extensiones.base_datos import obtener_sesion
from aplicacion.modelos.nucleo.usuarios import ConfiguracionEmpresa
from aplicacion.modelos.nucleo.roles import Rol
from aplicacion.modelos.nucleo.areas import Area

RUTA_MODELO = os.path.join(os.path.dirname(__file__),'..','..','modelos_ml', 'modelo_clasificador_erp.pkl')

try:
    modelo_ia = joblib.load(RUTA_MODELO)
except FileNotFoundError:
    modelo_ia = None
    print(f"Advertencia: No se encontró el modelo en {RUTA_MODELO}")

def predecir_modulos_con_ia(texto_usuario):
    if not modelo_ia:
        
        return {
            "ventas": True, "compras": False, "inventario": False,
            "produccion": False, "mantenimiento": False, "proyectos": False,
            "finanzas": False, "rrhh": False
        }
    
    
    prediccion = modelo_ia.predict([texto_usuario])[0]
    
    
    columnas = ["ventas", "compras", "inventario", "produccion", "mantenimiento", "proyectos", "finanzas", "rrhh"]
    
    modulos_generados = {}
    for i, modulo in enumerate(columnas):
        modulos_generados[modulo] = bool(prediccion[i])
        
    return modulos_generados

def bd_ia(usuario_id, negocio_nombre, texto_descripcion, modulos_str):

    sesion = obtener_sesion()

    
    config = ConfiguracionEmpresa(
        id_usuario=usuario_id,
        nombre_empresa=negocio_nombre,
        descripcion_empresa=texto_descripcion, 
        modulos_activados=modulos_str
    )

    sesion.add(config)
    sesion.commit()
    sesion.close()
    return True

def obtener_modulos_por_rol(rol):
    
    modulos_base = {
        "ventas": False, "compras": False, "inventario": False,
        "produccion": False, "mantenimiento": False, 
        "proyectos": False, "finanzas": False, "rrhh": False
    }
    
    mapa_roles = {
        "VENTAS": {"ventas": True},
        "COMPRAS": {"compras": True, "inventario": True},
        "ALMACEN": {"inventario": True},
        "PRODUCCION": {"produccion": True, "inventario": True},
        "MANTENIMIENTO": {"mantenimiento": True},
        "PROYECTOS": {"proyectos": True},
        "FINANZAS": {"finanzas": True, "ventas": True, "compras": True},
        "RRHH": {"rrhh": True}
    }
    
    permisos_rol = mapa_roles.get(rol.upper(), {})
    modulos_base.update(permisos_rol)
    
    return modulos_base



def sembrar_catalogos_iniciales(modulos_activados):
    
    semillas = {
        "ventas": {
            "areas": ["Piso de Ventas / Mostrador", "Atención a Clientes"],
            "roles": ["Cajero", "Gerente de Tienda", "Ejecutivo de Ventas"]
        },
        "inventario": {
            "areas": ["Almacén General", "Recepción de Mercancía"],
            "roles": ["Almacenista", "Jefe de Almacén"]
        },
        "produccion": {
            "areas": ["Planta de Producción", "Taller", "Control de Calidad"],
            "roles": ["Operario", "Supervisor de Producción", "Ingeniero de Calidad"]
        },
        "compras": {
            "areas": ["Oficina de Compras"],
            "roles": ["Comprador", "Gerente de Compras"]
        },
        "mantenimiento": {
            "areas": ["Departamento de Mantenimiento"],
            "roles": ["Técnico de Mantenimiento", "Jefe de Taller"]
        }
    }

    sesion = obtener_sesion()
    try:
        
        if not sesion.query(Area).filter_by(nombre_area="Dirección General").first():
            sesion.add(Area(nombre_area="Dirección General"))
        if not sesion.query(Rol).filter_by(nombre_rol="Administrador SGEA").first():
            sesion.add(Rol(nombre_rol="Administrador SGEA"))

       
        for modulo, activo in modulos_activados.items():
            if activo and modulo in semillas:
                
                # Crear Áreas si no existen
                for nombre_area in semillas[modulo]["areas"]:
                    existe = sesion.query(Area).filter_by(nombre_area=nombre_area).first()
                    if not existe:
                        sesion.add(Area(nombre_area=nombre_area))
                        
                # Crear Roles si no existen
                for nombre_rol in semillas[modulo]["roles"]:
                    existe = sesion.query(Rol).filter_by(nombre_rol=nombre_rol).first()
                    if not existe:
                        sesion.add(Rol(nombre_rol=nombre_rol))
                        
        sesion.commit()
        return True
    except Exception as e:
        sesion.rollback()
        print(f"--- ERROR AL SEMBRAR CATÁLOGOS ---: {e}")
        return False
    finally:
        sesion.close()