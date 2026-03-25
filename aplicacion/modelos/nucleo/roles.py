from aplicacion.modelos.base import *

class Rol(Base):
    __tablename__ = "roles"
    id_rol = Column(Integer, primary_key=True)
    nombre_rol = Column(String(50), nullable=False)