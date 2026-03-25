from aplicacion.modelos.base import *

class OrdenTrabajo(Base):
    __tablename__ = "ordenes_trabajo"
    id_orden = Column(Integer, primary_key=True)
    descripcion_falla = Column(Text)
    prioridad = Column(String(15))
    estado_orden = Column(String(20), default="Pendiente")
    id_tecnico = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_maquina = Column(Integer, ForeignKey("maquinas.id_maquina"))
