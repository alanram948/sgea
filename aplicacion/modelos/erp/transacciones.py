from aplicacion.modelos.base import *

class Transaccion(Base):
    __tablename__ = "erp_transacciones_bancarias"
    id_transaccion = Column(Integer, primary_key=True)
    tipo_transaccion = Column(String(20))
    id_socio = Column(Integer, ForeignKey("erp_socios_comerciales.id_socio"))
    id_documento_origen = Column(Integer, ForeignKey("erp_documentos.id_documento"))
    monto = Column(Numeric(15, 2))
    fecha_pago = Column(Date)
    referencia = Column(String(100))