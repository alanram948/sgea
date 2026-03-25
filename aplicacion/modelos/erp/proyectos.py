from aplicacion.modelos.base import *

class Proyecto(Base):
    __tablename__ = "erp_proyectos"
    id_proyecto = Column(Integer, primary_key=True)
    codigo_proyecto = Column(String(50), unique=True, nullable=False)
    nombre_proyecto = Column(String(200), nullable=False)
    id_socio_cliente = Column(Integer, ForeignKey("erp_socios_comerciales.id_socio"))
    presupuesto_estimado = Column(Numeric(15, 2), default=0.00)
    fecha_inicio = Column(Date)
    fecha_fin_estimada = Column(Date)
    porcentaje_avance = Column(Numeric(5, 2), default=0.00)
    estado = Column(String(20), default="Planificacion")