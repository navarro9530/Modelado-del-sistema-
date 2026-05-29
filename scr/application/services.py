#los servicios contiene la logica del negocio
#saben que hacer, pero le delegen a los repositorio como el crud


#responsabilidad de esta capa 
#orquetar la cominicacion con los repositorios
#aplicar las reglas de negosio 
#si esta en estado pendiente 
#trasformar los datos antes de retorno al api

#capi API= recibir las peticiones HTTP
#Servicio






from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from scr.domain.models import (Rol,Usuarios)
from scr.infraestructure.repository import (RolRepository, UsuarioRepository,BaseRepository)

#Rol service
class RolService:
    def __init__(self, db: Session):
        self.repo=RolRepository(db)

    def listar(self) -> List[Rol]:
        return self.repo.get_all()
    
    def obtener(self, id_rol: int) -> Optional[Rol]:
        return self.repo.get_by_id(id_rol)
    
    def crear(self, nombre_rol: str) -> Rol:
        nuevo_rol = Rol(nombre_rol=nombre_rol)
        return self.repo.create(nuevo_rol)
    
    def eliminar(self, id_rol: int) -> bool:
        return self.repo.delete(id_rol)


#Usuario service
class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def listar(self) -> List[Usuarios]:
        return self.repo.get_all()
    
    def obtener(self, id_usuario: int) -> Optional[Usuarios]:
        return self.repo.get_by_id(id_usuario)
    
    def obtener_nombre(self, nombre_usuario: str) -> Optional[Usuarios]:
        return self.repo.get_by_nombreUsuario(nombre_usuario)
    
    def obtener_correo(self, correo: str) -> Optional[Usuarios]:
        return self.repo.get_by_correo(correo)
    
    def crear(self, id_rol:int, nombre_completo: str, correo: str, password: str) -> Usuarios:
        nuevo_usuario = Usuarios(
            id_rol = id_rol,
            nombre_completo = nombre_completo, 
            correo = correo, 
            contrasena_hash = password
        )
        return self.repo.create(nuevo_usuario)

    def eliminar(self, id_usuario: int) -> bool:
        return self.repo.delete(id_usuario)
    
    def actualizar(self, id_usuario: int, **kwargs) -> Optional[Usuarios]:
        usuario = self.repo.get_by_id(id_usuario)
        if usuario:
            for key, value in kwargs.items():
                if value is not None:
                    setattr(usuario, key, value)
            return self.repo.update(usuario)
        return None