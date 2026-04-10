from datetime import datetime, timedelta
import random
import uuid
from aplicacion.extensiones.base_datos import obtener_sesion
from aplicacion.modelos.nucleo.usuarios import Usuario
from aplicacion.modelos.nucleo.roles import Rol
from aplicacion.modelos.nucleo.areas import Area
from aplicacion.modelos.erp.articulos import Articulo
from aplicacion.modelos.erp.documentos import Documento
from aplicacion.modelos.erp.lineas_documento import LineaDocumento 
from werkzeug.security import generate_password_hash

def inyectar_dummies_paleteria():
    sesion = obtener_sesion()
    try:
        rol_ventas = sesion.query(Rol).filter_by(nombre_rol="Cajero").first()
        if not rol_ventas:
            rol_ventas = Rol(nombre_rol="Cajero")
            sesion.add(rol_ventas)
        
        rol_almacen = sesion.query(Rol).filter_by(nombre_rol="Almacenista").first()
        if not rol_almacen:
            rol_almacen = Rol(nombre_rol="Almacenista")
            sesion.add(rol_almacen)

        area_ventas = sesion.query(Area).filter_by(nombre_area="Mostrador").first()
        if not area_ventas:
            area_ventas = Area(nombre_area="Mostrador")
            sesion.add(area_ventas)

        area_almacen = sesion.query(Area).filter_by(nombre_area="Bodega").first()
        if not area_almacen:
            area_almacen = Area(nombre_area="Bodega")
            sesion.add(area_almacen)
        
        sesion.commit()

        cajera = sesion.query(Usuario).filter_by(email="ana@empresa.com").first()
        if not cajera:
            cajera = Usuario(
                nombre_completo="Ana Lopez",
                email="ana@empresa.com",
                password=generate_password_hash("123"),
                id_rol=rol_ventas.id_rol,
                id_area=area_ventas.id_area
            )
            sesion.add(cajera)

        almacenista = sesion.query(Usuario).filter_by(email="beto@empresa.com").first()
        if not almacenista:
            almacenista = Usuario(
                nombre_completo="Beto Gomez",
                email="beto@empresa.com",
                password=generate_password_hash("123"),
                id_rol=rol_almacen.id_rol,
                id_area=area_almacen.id_area
            )
            sesion.add(almacenista)
        
        sesion.commit()

        articulos_db = []
        
        art_1 = sesion.query(Articulo).filter_by(codigo_sku="PAL-FRE").first()
        if not art_1:
            art_1 = Articulo(codigo_sku="PAL-FRE", descripcion="Paleta de Fresa", tipo_articulo="Producto Terminado", precio_venta_base=25.00, stock_actual=45)
            sesion.add(art_1)
        articulos_db.append(art_1)

        art_2 = sesion.query(Articulo).filter_by(codigo_sku="HEL-VAI").first()
        if not art_2:
            art_2 = Articulo(codigo_sku="HEL-VAI", descripcion="Helado Vainilla", tipo_articulo="Producto Terminado", precio_venta_base=120.00, stock_actual=15)
            sesion.add(art_2)
        articulos_db.append(art_2)

        art_3 = sesion.query(Articulo).filter_by(codigo_sku="AGU-HOR").first()
        if not art_3:
            art_3 = Articulo(codigo_sku="AGU-HOR", descripcion="Agua Horchata", tipo_articulo="Producto Terminado", precio_venta_base=35.00, stock_actual=30)
            sesion.add(art_3)
        articulos_db.append(art_3)

        sesion.commit()

        hoy = datetime.now()
        
        for _ in range(30):
            dias_atras = random.randint(0, 7)
            fecha_falsa = hoy - timedelta(days=dias_atras)
            folio_unico = f"T-{fecha_falsa.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
            
            nuevo_ticket = Documento(
                tipo_documento="TICKET",
                folio_documento=folio_unico,
                fecha_emision=fecha_falsa.date(),
                estado_documento="Pagado",
                id_usuario_creador=cajera.id_usuario,
                subtotal=0,
                total=0
            )
            sesion.add(nuevo_ticket)
            sesion.flush()

            total_ticket = 0
            
            for _ in range(random.randint(1, 3)):
                art_random = random.choice(articulos_db)
                cantidad = random.randint(1, 4)
                precio = art_random.precio_venta_base
                
                linea = LineaDocumento(
                    id_documento=nuevo_ticket.id_documento,
                    id_articulo=art_random.id_articulo,
                    cantidad=cantidad,
                    precio_unitario=precio,
                    porcentaje_descuento=0
                )
                sesion.add(linea)
                total_ticket += (float(cantidad) * float(precio))
                
            nuevo_ticket.subtotal = total_ticket
            nuevo_ticket.total = total_ticket

        sesion.commit()
        return "Dummies generados exitosamente."
        
    except Exception as e:
        sesion.rollback()
        return f"Error: {str(e)}"
    finally:
        sesion.close()
    sesion = obtener_sesion()
    
    empleados = [
        Usuario(nombre_completo="Ana López (Cajera)", email="ana@empresa.com", password=generate_password_hash("123"), id_rol=64, id_area=21),
        Usuario(nombre_completo="Beto Gómez (Almacén)", email="beto@empresa.com", password=generate_password_hash("123"), id_rol=65, id_area=22)
    ]
    sesion.add_all(empleados)
    sesion.commit()
    id_cajera = empleados[0].id_usuario

    articulos = [
        Articulo(codigo_sku="PAL-FRE", descripcion="Paleta de Fresa Natural", precio_venta_base=25.00, costo_estandar=10.00, stock_actual=45, stock_minimo=10, metodo_gestion="Ninguno"),
        Articulo(codigo_sku="HEL-VAI", descripcion="Litro Helado Vainilla", precio_venta_base=120.00, costo_estandar=50.00, stock_actual=15, stock_minimo=5, metodo_gestion="Lotes y Caducidad"),
        Articulo(codigo_sku="AGU-HOR", descripcion="Agua de Horchata 1L", precio_venta_base=35.00, costo_estandar=12.00, stock_actual=30, stock_minimo=10, metodo_gestion="Ninguno"),
        Articulo(codigo_sku="MAT-LEC", descripcion="Leche Entera (Litro)", precio_venta_base=0.00, costo_estandar=22.00, stock_actual=8, stock_minimo=20, metodo_gestion="Lotes y Caducidad")
    ]
    sesion.add_all(articulos)
    sesion.commit()

    hoy = datetime.now()
    for _ in range(30):
        dias_atras = random.randint(0, 7)
        fecha_falsa = hoy - timedelta(days=dias_atras)
        
        nuevo_ticket = Documento(
            tipo_documento="TICKET", folio=f"T-{random.randint(1000, 9999)}", 
            fecha_emision=fecha_falsa, total=0, estado="Pagado", id_usuario=id_cajera
        )
        sesion.add(nuevo_ticket)
        sesion.flush()

        total_ticket = 0
        
        for _ in range(random.randint(1, 3)):
            art_random = random.choice(articulos[:3])
            cantidad = random.randint(1, 4)
            precio = art_random.precio_venta_base
            total_linea = cantidad * precio
            total_ticket += total_linea
            
            sesion.add(LineaDocumento(id_documento=nuevo_ticket.id_documento, id_articulo=art_random.id_articulo, cantidad=cantidad, precio_unitario=precio))
            
        nuevo_ticket.total = total_ticket

    sesion.commit()
    sesion.close()
    return "Dummies inyectados con éxito"

