from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from aplicacion.modelos.base import Base

class LoteInventario(Base):
    __tablename__ = 'lotes_inventario'

    id_lote = Column(Integer, primary_key=True)
    id_articulo = Column(Integer, ForeignKey('erp_articulos.id_articulo', ondelete='CASCADE'), nullable=False)
    codigo_lote = Column(String(50), nullable=False)
    fecha_caducidad = Column(Date, nullable=False)
    cantidad_existente = Column(Numeric(12, 2), default=0.00)