import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scr"))

from scr.infraestructure.database import engine, Base
from scr.domain.models import Rol, Usuarios, Estudiante, Profesor, Monitor, Recurso

print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas exitosamente")
