from aplicacion.modelos.base import *

class ProduccionCalidad(Base):
    __tablename__ = "produccion_calidad"
    id_reporte = Column(Integer, primary_key=True)
    id_documento_erp = Column(Integer, ForeignKey("erp_documentos.id_documento"))
    piezas_producidas = Column(Integer)
    piezas_defectuosas = Column(Integer)
    fecha_reporte = Column(Date)
    id_supervisor = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_defecto_principal = Column(Integer, ForeignKey("catalogo_defectos.id_defecto"))