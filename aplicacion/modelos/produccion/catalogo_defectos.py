from aplicacion.modelos.base import *

class CatalogoDefecto(Base):
    __tablename__ = "catalogo_defectos"
    id_defecto = Column(Integer, primary_key=True)
    codigo = Column(String(10))
    descripcion = Column(String(100))
