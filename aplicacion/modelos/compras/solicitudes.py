from aplicacion.modelos.base import *

class SolicitudMaterial(Base):
    __tablename__ = "solicitudes_material"
    id_solicitud = Column(Integer, primary_key=True)
    id_articulo = Column(Integer, ForeignKey("erp_articulos.id_articulo"))
    cantidad = Column(Integer)
    costo_total_estimado = Column(Numeric(10, 2))
    justificacion = Column(Text)
    estado = Column(String(20), default="Pendiente")
    id_tecnico = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_autorizador = Column(Integer, ForeignKey("usuarios.id_usuario"))