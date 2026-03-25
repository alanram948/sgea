from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Numeric,
    ForeignKey, Date, DateTime, Text
)
from sqlalchemy.orm import declarative_base
from datetime import datetime
from aplicacion.extensiones.base_datos import motor
Base = declarative_base()