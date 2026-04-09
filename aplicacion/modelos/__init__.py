# Núcleo
from .nucleo.usuarios import Usuario
from .nucleo.roles import Rol
from .nucleo.areas import Area

# ERP
from .erp.socios import Socio
from .erp.articulos import Articulo
from .erp.proyectos import Proyecto
from .erp.documentos import Documento
from .erp.lineas_documento import LineaDocumento
from .erp.transacciones import Transaccion

# Mantenimiento
from .mantenimiento.maquinas import Maquina
from .mantenimiento.ordenes import OrdenTrabajo

# Producción
from .produccion.calidad import ProduccionCalidad
from .produccion.catalogo_defectos import CatalogoDefecto

# compras
from .compras.solicitudes import SolicitudMaterial

# Auditoría
from .auditoria.movimientos import Auditoria

#cuestionario
from .nucleo.usuarios import ConfiguracionEmpresa