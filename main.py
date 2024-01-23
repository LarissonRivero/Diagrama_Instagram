from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String, unique=True, nullable=False)
    correo_electronico = Column(String, unique=True, nullable=False)
    contraseña = Column(String, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    publicaciones = relationship('Publicacion', back_populates='usuario')
    me_gustas = relationship('MeGusta', back_populates='usuario')

class Publicacion(Base):
    __tablename__ = 'publicaciones'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    imagen = Column(String, nullable=False)
    descripcion = Column(Text)
    fecha_publicacion = Column(DateTime, default=datetime.utcnow)

    usuario = relationship('Usuario', back_populates='publicaciones')
    comentarios = relationship('Comentario', back_populates='publicacion')
    me_gustas = relationship('MeGusta', back_populates='publicacion')

class Comentario(Base):
    __tablename__ = 'comentarios'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    publicacion_id = Column(Integer, ForeignKey('publicaciones.id'), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    usuario = relationship('Usuario', back_populates='comentarios')
    publicacion = relationship('Publicacion', back_populates='comentarios')

class MeGusta(Base):
    __tablename__ = 'me_gustas'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    publicacion_id = Column(Integer, ForeignKey('publicaciones.id'), nullable=False)

    usuario = relationship('Usuario', back_populates='me_gustas')
    publicacion = relationship('Publicacion', back_populates='me_gustas')

DATABASE_URL = "sqlite:///instagram.db"
engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    sql_script = connection.connection.driver_connection._generate_create_table()
    with open('create_tables.sql', 'w') as sql_file:
        sql_file.write(sql_script)
