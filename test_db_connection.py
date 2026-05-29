import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scr"))

from scr.infraestructure.database import engine, SessionLocal, DATABASE_URL

from sqlalchemy import text


def test_db_connection():
    print(f"Intentando conectar a la base de datos: {DATABASE_URL}\n")

    #1. probar el enegine directamente
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM ROLES"))
            print("Enegie conecado correctamente:")
            print(f"Resultado SELECT 1 : {result.fetchall()}")
    except Exception as e:
        print(f"Error al conectar con el engine: {e}")
        return
    
    print("\nProbando la pruebas pasaron. la DB esta operativa.")

test_db_connection()