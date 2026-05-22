#capas de dominio, donde se definen las entidades y la lógica de negocio de la aplicación
#es como un espejo que comunica BD con python
#una tabla equivale a una clase 

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

#importamos la clase base desde la capa de infraestructura para heredarla en nuestras clases de modelo
from scr.infraestructure.database import Base


#====================
#ROL
#=====================
class Rol(Base):
    __tablename__ = "ROLES"

    #primary key, autoincrementable
    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre_rol = Column(String(50))

    #relacion inversa:desde rol poedmos acceder a la lista usuarios
    usuarios = relationship("Usuarios", back_populates="rol")

    
#====================
#USUARIOS
#=====================

class Usuarios(Base):
    __tablename__ = "USUARIOS"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    #FK heredada de la tabla ROLES
    id_rol = Column(Integer, ForeignKey("ROLES.id_rol"))
    nombre_usuario = Column(String(150))
    correo = Column(String(100), unique=True)
    contrasena_hash = Column(String(255))

    #relacion hacia la tabla ROLES y hacia las tablas hijas 
    rol = relationship("Rol", back_populates="usuarios")

    estudiante = relationship("Estudiante", back_populates="usuario", uselist=False)
    profesor = relationship("Profesor", back_populates="usuario", uselist=False)
    monitor = relationship("Monitor", back_populates="usuario", uselist=False)
    reservas = relationship("Reserva", back_populates="usuario")


#====================
#ESTUDIANTE 
#=====================
class Estudiante(Base):
    __tablename__ = "ESTUDIANTES"
    #al ser PK y FK a la vez, en este caso se vincula al estudiante con el usuario correspondiente
    id_usuario = Column(Integer, ForeignKey("USUARIOS.id_usuario"), primary_key=True)
    matricula = Column(String(50), unique=True)
    programa_academico = Column(String(100))

    usuario = relationship("Usuarios", back_populates="estudiante")


#====================
#PROFESOR
#=====================
class Profesor(Base):
    __tablename__ = "PROFESORES"

    id_usuario = Column(Integer, ForeignKey("USUARIOS.id_usuario"), primary_key=True)
    departamento = Column(String(100))

    usuario = relationship("Usuarios", back_populates="profesor")

#====================
#MONITOR
#=====================
class Monitor(Base):
    __tablename__ = "MONITORES"

    id_usuario = Column(Integer, ForeignKey("USUARIOS.id_usuario"), primary_key=True)
    id_turno = Column(Integer)

    usuario = relationship("Usuarios", back_populates="monitor")

#====================
#RECURSOS
#=====================
class Recurso(Base):
    __tablename__ = "RECURSOS"

    id_recurso = Column(Integer, primary_key=True, autoincrement=True)
    id_placa = Column(String(50), unique=True)
    marca = Column(String(100))
    estado = Column(String(50))
    tipo_recurso = Column(String(50))

    laboratorios = relationship("Laboratorios", back_populates="recurso", uselist=False)
    equipos = relationship("Equipos", back_populates="recurso", uselist=False)
    reservas = relationship("Reserva", back_populates="recurso")
    novedades = relationship("Novedad", back_populates="recurso")


#====================
#LABORATORIOS
#=====================
class Laboratorios(Base):
    __tablename__ = "LABORATORIOS"

    id_recurso = Column(Integer, ForeignKey("RECURSOS.id_recurso"), primary_key=True)
    capacidad = Column(Integer)
    software = Column(String(255))
    ubicacion = Column(String(100))

    recurso = relationship("Recurso", back_populates="laboratorios")

#==================== 
#EQUIPOS
#=====================
class Equipos(Base):
    __tablename__ = "EQUIPOS_PORTATILES"

    id_recurso = Column(Integer, ForeignKey("RECURSOS.id_recurso"), primary_key=True)
    modelo = Column(String(100))
    sistema_operativo = Column(String(100))

    recurso = relationship("Recurso", back_populates="equipos")

#====================
#RESERVAS
#===================== 
class Reserva(Base):
    __tablename__ = "RESERVAS"

    id_reserva = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("USUARIOS.id_usuario"))
    id_recurso = Column(Integer, ForeignKey("RECURSOS.id_recurso"))
    fecha_reserva = Column(DateTime)

    usuario = relationship("Usuarios", back_populates="reservas")
    recurso = relationship("Recurso", back_populates="reservas")

#==================== 
#NOVEDADES  
#=====================
class Novedad(Base):
    __tablename__ = "NOVEDADES"

    id_novedad = Column(Integer, primary_key=True, autoincrement=True)
    id_recurso = Column(Integer, ForeignKey("RECURSOS.id_recurso"))
    descripcion = Column(String(255))
    fecha_novedad = Column(DateTime)

    recurso = relationship("Recurso", back_populates="novedades")
