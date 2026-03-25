from aplicacion.modelos.base import *


class Area(Base):
    __tablename__ = "areas"
    id_area = Column(Integer, primary_key=True)
    nombre_area = Column(String(50), nullable=False)