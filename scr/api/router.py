#Aqui esta definico los endpoints HTTP
#Es la capa mas externa de nuetro modelo 
#es la que recibe las peticiones 
#es la que retorna los datos


#metodos HTTP: GET, POST, PUT, DELETE
#GET: obtener datos(select)
#POST: crear un nuevo recurso(insert)
#PUT: actualizar un recurso existente(update)
#DELETE: eliminar un recurso existente(delete)
#PATCH: actualizar parcialmente un recurso existente(update)

#CODIGOS DE RESPUESTA HTTP
#200 OK: GET - PUT - DELETE exitoso
#201 Created: POST exitoso
#204 No Content: DELETE exitoso sin contenido de respuesta
#404 Not Found: recurso no encontrado


#Depends(get_db)
#FastApi inyecta la dependencia de la base de datos en cada endpoint, lo que permite acceder a la sesión de la base de datos dentro de las funciones del endpoint sin tener que crearla manualmente cada vez. Esto facilita la gestión de la conexión a la base de datos y asegura que se cierre correctamente después de cada solicitud.


from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from typing import List


from scr.infraestructure.database import get_db

from scr.application.services import (RolService,UsuarioService)

from scr.api.schemas import (RolCreate,RolResponse,UsuarioCreate,UsuarioResponse,UsuarioUpdate)

#API Router, que agrupa las rutas 
#Asigna un versionado a la API, en este caso v1
router = APIRouter(prefix="/api/v1")

#Rol
@router.get("/roles", response_model=List[RolResponse], tags=["Roles"])
def listar_roles(db: Session = Depends(get_db)):
    return RolService(db).listar()

@router.get("/roles/{id_rol}", response_model=RolResponse, tags=["Roles"])
def obtener_rol(id_rol: int, db: Session = Depends(get_db)):
    rol = RolService(db).obtener(id_rol)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.post("/roles", response_model=RolResponse, status_code=status.HTTP_201_CREATED, tags=["Roles"])
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
    return RolService(db).crear(rol.nombre_rol)

@router.delete("/roles/{id_rol}", status_code=status.HTTP_204_NO_CONTENT, tags=["Roles"])
def eliminar_rol(id_rol: int, db: Session = Depends(get_db)):
    if not RolService(db).obtener(id_rol):
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    RolService(db).eliminar(id_rol)
    

#Usuario
@router.get("/usuarios", response_model=List[UsuarioResponse], tags=["Usuarios"])
def listar_usuarios(db: Session = Depends(get_db)):
    return UsuarioService(db).listar()

@router.get("/usuarios/{id_usuario}", response_model=UsuarioResponse, tags=["Usuarios"])
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = UsuarioService(db).obtener(id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return UsuarioService(db).crear(usuario.id_rol, usuario.nombre_completo, usuario.correo, usuario.contrasena_hash)

@router.delete("/usuarios/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT, tags=["Usuarios"])
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    if not UsuarioService(db).obtener(id_usuario):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    

@router.put("/usuarios/{id_usuario}", response_model=UsuarioResponse, tags=["Usuarios"])
def actualizar_usuario(id_usuario: int, data : UsuarioUpdate, db: Session = Depends(get_db)):
    #cuando se actauliza un usuario, se puede actualizar cualquier campo, por eso se usa el exclude_unset=True para que solo se actualicen los campos que se envian en la peticion, si no se envia un campo, no se actualiza
    usuario = UsuarioService(db).actualizar(id_usuario, **data.model_dump(exclude_unset=True))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
