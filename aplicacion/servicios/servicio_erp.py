from aplicacion.extensiones.base_datos import obtener_sesion
from aplicacion.modelos.nucleo.usuarios import ConfiguracionEmpresa
def obtener_nombre():
    sesion=obtener_sesion()
    configuracion=sesion.query(ConfiguracionEmpresa).first()
    nombre=configuracion.nombre_empresa
    sesion.close()
    return nombre
    