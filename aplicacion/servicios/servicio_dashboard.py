from datetime import datetime, timedelta
from sqlalchemy import func, cast, Date
from aplicacion.extensiones.base_datos import obtener_sesion
from aplicacion.modelos.erp.documentos import Documento

def obtener_ventas_semanal():
    sesion = obtener_sesion()
    hoy = datetime.now().date()

    fechas_grafica=[]
    ventas_grafica=[]
    ventas_hoy=0
    try:
        for i in range(6,-1,-1):
            dia_objetivo=hoy-timedelta(days=i)

            fechas_grafica.append(dia_objetivo.strftime("%d/%m"))
            total_dia = sesion.query(func.sum(Documento.total)).filter(
                    cast(Documento.fecha_emision, Date) == dia_objetivo,
                    Documento.tipo_documento == "TICKET",
                    Documento.estado_documento == "Pagado" 
                ).scalar()
            tickets_hoy = sesion.query(Documento).filter(
                    cast(Documento.fecha_emision, Date) == dia_objetivo,
                    Documento.tipo_documento == "TICKET",
                    Documento.estado_documento == "Pagado"
                ).count()
            total_dia = float(total_dia or 0.0)
            ventas_grafica.append(total_dia)
            if i == 0: 
                    ventas_hoy = total_dia
        return {
            "fechas": fechas_grafica,
            "ventas": ventas_grafica,
            "ventas_hoy": ventas_hoy,
            "tickets_hoy": tickets_hoy
        }
    finally:
         sesion.close()