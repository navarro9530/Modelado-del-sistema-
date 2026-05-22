#este archivo es el responsable de establecer la conexion xon la base de datos
#MySQL usando SQLAlchemy como nuestro ORM ( Object-Relational Mapping)
#convuerte tablas de mysql a clases de python

#3 conceptos claves
#Engine: representa la conexion fisica al motor de la base de datos
#Sesion: Unidad de trabajo que acomula operaciones antes de enviarlas a la DB
#Base: Clase padre de la cual heredan todos los modelos del ORM

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#cargar las variables definidas en el archivo .env al entorno del proceso
load_dotenv()
#esto evita tener que escribir las varibles directamente

#esta es la cadena de conexion
DATABASE_URL = (f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME')}")

#creamos el Engine
engine = create_engine(DATABASE_URL,pool_pre_ping=True)

#creamos la sesion
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#declaramos la base
#Heredar todos lode modelos del ORM
Base = declarative_base()

#utlizamos un generador que provee una sesion de DB a cada enpoiont de fastapo
#get_db

def get_db():
    db = SessionLocal() #Abre una nueva sesion
    try:
        yield db #Entregar la sesion al endpoint que la solicito
    finally:
        db.close() #Cierra la sesion 
