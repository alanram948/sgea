from aplicacion.modelos.base import *

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True)
    id_socio = Column(Integer, ForeignKey("erp_socios_comerciales.id_socio"))
    nombre_completo = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    password = Column(String(255), nullable=False)
    fecha_contratacion = Column(Date)
    salario_mensual = Column(Numeric(10, 2), default=8000.00)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"))
    id_area = Column(Integer, ForeignKey("areas.id_area"))
    id_supervisor = Column(Integer, ForeignKey("usuarios.id_usuario"))
