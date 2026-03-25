from aplicacion.modelos.base import *

class Documento(Base):
    __tablename__ = "erp_documentos"
    id_documento = Column(Integer, primary_key=True)
    tipo_documento = Column(String(50), nullable=False)
    folio_documento = Column(String(50), unique=True, nullable=False)
    id_socio = Column(Integer, ForeignKey("erp_socios_comerciales.id_socio"))
    fecha_emision = Column(Date)
    fecha_vencimiento = Column(Date)
    estado_documento = Column(String(30), default="Abierto")
    moneda = Column(String(3), default="MXN")
    subtotal = Column(Numeric(15, 2), default=0.00)
    impuestos = Column(Numeric(15, 2), default=0.00)
    total = Column(Numeric(15, 2), default=0.00)
    id_proyecto = Column(Integer, ForeignKey("erp_proyectos.id_proyecto"))
    id_usuario_creador = Column(Integer, ForeignKey("usuarios.id_usuario"))