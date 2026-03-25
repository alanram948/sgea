from aplicacion.modelos.base import *

class Maquina(Base):
    __tablename__ = "maquinas"
    id_maquina = Column(Integer, primary_key=True)
    id_articulo = Column(Integer, ForeignKey("erp_articulos.id_articulo"))
    nombre_maquina = Column(String(100))
    modelo = Column(String(50))
    estado = Column(String(20), default="Operativa")
    id_area = Column(Integer, ForeignKey("areas.id_area"))