from aplicacion.extensiones.base_datos import obtener_sesion
from aplicacion.modelos.erp.articulos import Articulo
from aplicacion.modelos.erp.lotes import LoteInventario
from aplicacion.modelos.erp.documentos import Documento
from aplicacion.modelos.erp.lineas_documento import LineaDocumento 
import uuid

def venta(datos, id_usuario):
    carrito = datos.get("items", [])
    total = datos.get("total", 0)
    
    

    sesion = obtener_sesion()
    try:
        
        folio_nuevo = f"TKT-{str(uuid.uuid4())[:6].upper()}"
        
        nuevo_documento = Documento(
            tipo_documento="Ticket de Venta",
            folio_documento=folio_nuevo,
            estado_documento="Cerrado",
            subtotal=total, 
            total=total,
            id_usuario_creador=id_usuario
        )
        sesion.add(nuevo_documento)
        sesion.flush() 
        
        
        for item in carrito:
            nueva_linea = LineaDocumento(
                id_documento=nuevo_documento.id_documento,
                id_articulo=item["id_articulo"],
                cantidad=item["cantidad"],
                precio_unitario=item["precio_unitario"]
            )
            sesion.add(nueva_linea)
            
            articulo = sesion.query(Articulo).get(item["id_articulo"])
            
            if articulo:
                cantidad_venta = float(item["cantidad"])
                
                # Descuento general seguro
                articulo.stock_actual = float(articulo.stock_actual or 0) - cantidad_venta
                
                # Descuento por Lotes (FIFO)
                if articulo.metodo_gestion == "Lotes y Caducidad":
                    lotes = sesion.query(LoteInventario).filter(
                        LoteInventario.id_articulo == articulo.id_articulo,
                        LoteInventario.cantidad_existente > 0
                    ).order_by(LoteInventario.fecha_caducidad.asc()).all()

                    for lote in lotes:
                        if cantidad_venta <= 0:
                            break 
                            
                        existencia_lote = float(lote.cantidad_existente or 0)

                        if existencia_lote >= cantidad_venta:
                            lote.cantidad_existente = existencia_lote - cantidad_venta
                            cantidad_venta = 0
                        else:
                            cantidad_venta -= existencia_lote
                            lote.cantidad_existente = 0
                
        
        sesion.commit()
        return {"exito": True, "folio": folio_nuevo}, 200
        
    except Exception as e:
        sesion.rollback()
        return {"exito": False, "error": "Error interno al guardar la venta. Revisa la consola."}, 500
    finally:
        sesion.close()
