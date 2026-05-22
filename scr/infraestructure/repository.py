#El repositorio encapsula las consultas SQL
#solo sabe como guardar,recuperar,eliminar y modificar los datos
#pero no sabe por que 

from typing import List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from scr.domain.models import (Rol,Usuarios, Estudiante, Profesor, Monitor)

#se usa para que el tipo de retorno de los archivos genericosse aconsistente
#con el modelo (rol usuario,esteudiante,profesor,monitor)
T = TypeVar("T")



class BaseRepository:
    def __init__(self, model:Type, db:Session):
        self.model = model
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List:
        #offset: se salta los primeros n registros, limit: limita el numero de registros devueltos
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def get_by_id(self, record_id: int) -> Optional[object]:
        #si no encuentra el registro devuelve None
        pk = self.model.__mapper__.primary_key[0].name #obtiene la columna de la clave primaria
        return self.db.query(self.model).filter(getattr(self.model, pk) == record_id).first()

    def create(self, obj) -> object:
        self.db.add(obj) # agrega el objeto a la sesión de la base de datos
        self.db.commit() # Enviamos el insert a la base de datosy se cpnfirma
        self.db.refresh(obj) # recaargar el objeto a la base de datos 
        return obj

    def update(self, obj) -> object:
        self.db.merge(obj) # fusiona el estado del objeto con la sesión de la base de datos
        self.db.commit() # confirma los cambios en la base de datos
        self.db.refresh(obj)
        return obj

    def delete(self, record_id: int) -> bool:
        obj = self.get_by_id(record_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
    

#Metodos especificos

class RolRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Rol, db)

    def get_by_name(self, nombre: str) -> Optional[Rol]:
        return self.db.query(Rol).filter(Rol.nombre_rol == nombre).first()
    
class UsuarioRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Usuarios, db)

    def get_by_nombreUsuario(self, nombre: str) -> Optional[Usuarios]:
        return self.db.query(Usuarios).filter(Usuarios.nombre_completo == nombre).first() 

    def get_by_correo(self, correo: str) -> Optional[Usuarios]:
        return self.db.query(Usuarios).filter(Usuarios.correo == correo).first()


    