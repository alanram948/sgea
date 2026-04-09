from aplicacion.extensiones.base_datos import obtener_sesion
from aplicacion.modelos.erp.articulos import Articulo
from aplicacion.modelos.erp.lotes import LoteInventario
from flask import Blueprint, render_template, request, redirect, url_for, session


def registrar_articulo(datos_formulario):
    sesion = obtener_sesion()
    se_compra = True if datos_formulario.get("se_compra") else False
    se_vende = True if datos_formulario.get("se_vende") else False
    se_inventaria = True if datos_formulario.get("se_inventaria") else False
    nuevo_articulo = Articulo(
            codigo_sku=datos_formulario.get("codigo_sku"),
            descripcion=datos_formulario.get("descripcion"),
            tipo_articulo=datos_formulario.get("tipo_articulo"),
            metodo_gestion=datos_formulario.get("metodo_gestion", "Ninguno"),
            costo_estandar=float(datos_formulario.get("costo_estandar", 0)),
            precio_venta_base=float(datos_formulario.get("precio_venta_base", 0)),
            se_compra=se_compra,
            se_vende=se_vende,
            se_inventaria=se_inventaria,
            stock_actual=0.00,
            stock_minimo=float(datos_formulario.get("stock_minimo", 0)),
            estado="Activo"
        )

    try:
        sesion.add(nuevo_articulo)
        sesion.commit()
        return True
    except Exception as e:
        sesion.rollback()
        print(f"Error al guardar el artículo: {e}")
        return False
    finally:
        sesion.close()

def obtener_inventario():
    sesion = obtener_sesion()
    productos = sesion.query(Articulo).all()
    sesion.close()
    return productos
def obtener_articulo(id):
    sesion=obtener_sesion()
    articulo = sesion.query(Articulo).get(id)
    return articulo

def articulo_lote(id,cantidad_nueva):
    sesion = obtener_sesion()
    articulo = sesion.query(Articulo).get(id)
    articulo.stock_actual = float(articulo.stock_actual or 0) + float(cantidad_nueva)

    if articulo.metodo_gestion == "Lotes y Caducidad":
            nuevo_lote = LoteInventario(
                id_articulo=articulo.id_articulo,
                codigo_lote=request.form.get("codigo_lote"),
                fecha_caducidad=request.form.get("fecha_caducidad"),
                cantidad_existente=cantidad_nueva
            )
            sesion.add(nuevo_lote)

    sesion.commit()
    sesion.close()
    