from aplicacion.modelos.base import *

class Articulo(Base):
    __tablename__ = "erp_articulos"
    id_articulo = Column(Integer, primary_key=True)
    codigo_sku = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=False)
    tipo_articulo = Column(String(30), nullable=False)
    metodo_gestion = Column(String(20), default="Ninguno")
    costo_estandar = Column(Numeric(12, 2), default=0.00)
    precio_venta_base = Column(Numeric(12, 2), default=0.00)
    se_compra = Column(Boolean, default=True)
    se_vende = Column(Boolean, default=True)
    se_inventaria = Column(Boolean, default=True)
    stock_actual = Column(Numeric(12, 2), default=0.00)
    stock_minimo = Column(Numeric(12, 2), default=5.00)
    estado = Column(String(20), default="Activo")

