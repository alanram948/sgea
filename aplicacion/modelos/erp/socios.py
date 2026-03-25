from aplicacion.modelos.base import *

class Socio(Base):
    __tablename__ = "erp_socios_comerciales"
    id_socio = Column(Integer, primary_key=True)
    codigo_socio = Column(String(50), unique=True, nullable=False)
    razon_social = Column(String(200), nullable=False)
    rfc_tax_id = Column(String(50))
    es_cliente = Column(Boolean, default=False)
    es_proveedor = Column(Boolean, default=False)
    es_empleado = Column(Boolean, default=False)
    es_lead = Column(Boolean, default=False)
    email_principal = Column(String(100))
    limite_credito = Column(Numeric(15, 2), default=0.00)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    estado = Column(String(20), default="Activo")