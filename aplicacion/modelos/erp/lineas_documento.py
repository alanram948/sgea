from aplicacion.modelos.base import *

class LineaDocumento(Base):
    __tablename__ = "erp_lineas_documento"
    id_linea = Column(Integer, primary_key=True)
    id_documento = Column(Integer, ForeignKey("erp_documentos.id_documento"))
    id_articulo = Column(Integer, ForeignKey("erp_articulos.id_articulo"))
    descripcion_linea = Column(Text)
    cantidad = Column(Numeric(12, 4))
    precio_unitario = Column(Numeric(15, 2), default=0.00)
    porcentaje_descuento = Column(Numeric(5, 2), default=0.00)