from aplicacion.modelos.base import *

class Auditoria(Base):
    __tablename__ = "auditoria_logs"
    id_log = Column(Integer, primary_key=True)
    evento = Column(String(255))
    usuario_responsable = Column(String(100))
    fecha_hora = Column(DateTime, default=datetime.utcnow)