from aplicacion.extensiones.base_datos import obtener_sesion

try:
    sesion = obtener_sesion()
    print("Conexión a la base de datos exitosa")
    sesion.close()
except Exception as e:
    print("Error de conexión:")
    print(e)