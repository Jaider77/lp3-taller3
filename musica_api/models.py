"""
Módulo de modelos de datos para la aplicación.
Define las clases de modelos SQLAlchemy que representan las tablas de la base de datos.
"""
from .extensions import db
from datetime import datetime

class Usuario(db.Model):
    """
    Modelo para representar un usuario en el sistema.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    contrasena = db.Column(db.String(255), nullable=False)  # <--- AGREGA ESTA LÍNEA
    
    # Relación con favoritos
    favoritos = db.relationship("Favorito", back_populates="usuario", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Usuario {self.nombre}>"

class Cancion(db.Model):
    """
    Modelo para representar una canción en el sistema.
    """
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    artista = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(200))
    duracion = db.Column(db.Integer)  # Duración en segundos
    año = db.Column(db.Integer)
    genero = db.Column(db.String(50))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con favoritos
    favoritos = db.relationship("Favorito", back_populates="cancion", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Cancion {self.titulo} - {self.artista}>"

class Favorito(db.Model):
    """
    Modelo para representar una relación de favorito entre un usuario y una canción.
    """
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    id_cancion = db.Column(db.Integer, db.ForeignKey("cancion.id"), nullable=False)
    fecha_marcado = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = db.relationship("Usuario", back_populates="favoritos")
    cancion = db.relationship("Cancion", back_populates="favoritos")
    
    # Índice único para evitar duplicados
    __table_args__ = (
        db.UniqueConstraint('id_usuario', 'id_cancion', name='uq_usuario_cancion'),
    )
    
    def __repr__(self):
        return f"<Favorito: Usuario {self.id_usuario} - Canción {self.id_cancion}>"

