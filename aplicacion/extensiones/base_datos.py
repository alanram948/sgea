import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import session

# Cargar variables del .env
load_dotenv()

USUARIO = os.getenv("USUARIO_BD")
CLAVE = os.getenv("CLAVE_BD")
HOST = os.getenv("HOST_BD")
PUERTO = os.getenv("PUERTO_BD")
NOMBRE = os.getenv("NOMBRE_BD")

# URL de conexión
URL_BD = f"postgresql://{USUARIO}:{CLAVE}@{HOST}:{PUERTO}/{NOMBRE}"

# Motor de conexión
motor = create_engine(URL_BD, echo=True)

# Sesiones
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)

# Obtener sesión
def obtener_sesion():
    return SesionLocal()
def obtener_modulos():
    modulos=session.get("modulos")
    if not modulos:
        return {
            "ventas": False,
            "inventario": False,
            "produccion": False,
            "finanzas": False
        }

    return modulos