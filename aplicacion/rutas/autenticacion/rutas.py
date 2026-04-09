from flask import Blueprint, render_template, request, redirect, url_for, session
from aplicacion.servicios.servicio_autenticacion import validar_usuario, registrar_usuario, marcar_configuracion_completa, buscar_lider
from aplicacion.servicios.servicio_ia import bd_ia, obtener_modulos_por_rol, predecir_modulos_con_ia, sembrar_catalogos_iniciales
from aplicacion.modelos.nucleo.usuarios import ConfiguracionEmpresa
from aplicacion.extensiones.base_datos import obtener_sesion
from werkzeug.security import generate_password_hash
autenticacion_bp = Blueprint('autenticacion', __name__)

@autenticacion_bp.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        email = request.form["usuario"]
        contrasena = request.form["contrasena"]
        usuario = validar_usuario(email, contrasena)

        if usuario:
            session["usuario_id"] = usuario["Id"]
            rol_usuario = usuario["Rol"].upper()
            session["rol"] = rol_usuario

            # --- CONTROL DE MÓDULOS ---
            if rol_usuario == "LIDER":
                sesion_bd = obtener_sesion()
                config = sesion_bd.query(ConfiguracionEmpresa).filter_by(id_usuario=usuario["Id"]).first()
                sesion_bd.close()
                
                if config and config.modulos_activados:
                    lista_modulos = config.modulos_activados.split(',')
                    session["modulos"] = {mod: True for mod in lista_modulos}
                else:
                    return redirect("/cuestionario") 
            else:
                session["modulos"] = obtener_modulos_por_rol(rol_usuario)

            return redirect("/panel")
        else:
            return "Credenciales incorrectas"

    return render_template("autenticacion/inicio_sesion.html", mostrar_sidebar=False)



@autenticacion_bp.route("/registro", methods=["GET", "POST"])
def registro():
    existe_lider = buscar_lider()

    if existe_lider:
        return redirect("/login")

    if request.method == "POST":

        # datos
        nombre = request.form["nombre"]
        email = request.form["email"]
        contrasena = request.form["contrasena"]


        usuario_id = registrar_usuario(nombre, email, contrasena, "LIDER")
        session.clear()
        session["usuario_id"]=usuario_id
        session["rol"]="LIDER"
        
        return redirect("/cuestionario")


    return render_template("autenticacion/registro.html")
 
@autenticacion_bp.route("/cuestionario", methods=["GET", "POST"])
def cuestionario_ia():
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return redirect(url_for("autenticacion.login"))

    if request.method == "POST":
        nombre_empresa = request.form.get("nombre_empresa", "Mi Empresa")
    
        q2_tipo_venta = request.form.get("q2_tipo_venta", "")
        q3_origen = request.form.get("q3_origen", "")
        q4_caducidad = request.form.get("q4_caducidad", "")
        q5_mantenimiento = request.form.get("q5_mantenimiento", "")
        texto_libre_ia = request.form.get("q6_extra", "")

        
        modulos = {
            "ventas": True,
            "inventario": "No manejo" not in q4_caducidad,
            "produccion": "fabricamos" in q3_origen.lower(),
            "compras": "proveedores" in q3_origen.lower() or "materia prima" in q3_origen.lower(),
            "mantenimiento": "Sí" in q5_mantenimiento
        }
        if len(texto_libre_ia.strip()) > 10:
            sugerencias_ia = predecir_modulos_con_ia(texto_libre_ia)
            if sugerencias_ia.get("produccion"): modulos["produccion"] = True
            if sugerencias_ia.get("mantenimiento"): modulos["mantenimiento"] = True
            if sugerencias_ia.get("inventario"): modulos["inventario"] = True   

        modulos_texto = ",".join([mod for mod, activo in modulos.items() if activo])
        


        bd_ia(usuario_id, nombre_empresa, texto_libre_ia, modulos_texto)
        sembrar_catalogos_iniciales(modulos)
        marcar_configuracion_completa(usuario_id)
        session["modulos"] = modulos
        session["nombre_empresa"] = nombre_empresa
        return redirect("/panel")

    return render_template("autenticacion/cuestionario.html", mostrar_sidebar=False)
    


