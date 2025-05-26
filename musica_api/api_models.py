"""
Módulo de modelos de API para la serialización/deserialización de datos.
Define los esquemas utilizados por Flask-RESTX para la documentación y validación.
"""
from flask_restx import fields
from .extensions import api

#modelo para mostrar los usurios
usuario_model = api.model('Usuario', {
    'id': fields.Integer,
    'nombre': fields.String,
    'correo': fields.String,
})
# Modelo para respuestas simples
mensaje_model = api.model("Mensaje", {
    "mensaje": fields.String(description="Mensaje informativo")
})

# Modelos para Usuario
usuario_base = api.model("UsuarioBase", {
    "nombre": fields.String(required=True, description="Nombre del usuario"),
    "correo": fields.String(required=True, description="Correo electrónico del usuario")
})

usuario_model = api.inherit("Usuario", usuario_base, {
    "id": fields.Integer(description="Identificador único del usuario"),
    "fecha_registro": fields.DateTime(description="Fecha de registro del usuario")
})

# Modelos para Canción
cancion_base = api.model("CancionBase", {
    "titulo": fields.String(required=True, description="Título de la canción"),
    "artista": fields.String(required=True, description="Artista/intérprete de la canción"),
    "album": fields.String(description="Álbum al que pertenece la canción"),
    "duracion": fields.Integer(description="Duración en segundos"),
    "año": fields.Integer(description="Año de lanzamiento"),
    "genero": fields.String(description="Género musical")
})

cancion_model = api.inherit("Cancion", cancion_base, {
    "id": fields.Integer(description="Identificador único de la canción"),
    "fecha_creacion": fields.DateTime(description="Fecha de creación del registro")
})

# Modelos para Favorito
favorito_input = api.model("FavoritoInput", {
    "id_usuario": fields.Integer(required=True, description="ID del usuario"),
    "id_cancion": fields.Integer(required=True, description="ID de la canción")
})

# Modelo para mostrar detalles completos de un favorito
cancion_simple = api.model("CancionSimple", {
    "id": fields.Integer(description="ID de la canción"),
    "titulo": fields.String(description="Título de la canción"),
    "artista": fields.String(description="Artista de la canción")
})

usuario_simple = api.model("UsuarioSimple", {
    "id": fields.Integer(description="ID del usuario"),
    "nombre": fields.String(description="Nombre del usuario")
})

favorito_model = api.model("Favorito", {
    "id": fields.Integer(description="ID del favorito"),
    "id_usuario": fields.Integer(description="ID del usuario"),
    "id_cancion": fields.Integer(description="ID de la canción"),
    "fecha_marcado": fields.DateTime(description="Fecha en que se marcó como favorito"),
    "usuario": fields.Nested(usuario_simple, description="Datos del usuario"),
    "cancion": fields.Nested(cancion_simple, description="Datos de la canción")
})

# Modelo para mostrar canciones favoritas de un usuario
favoritos_usuario_model = api.model("FavoritosUsuario", {
    "usuario": fields.Nested(usuario_simple),
    "canciones_favoritas": fields.List(fields.Nested(cancion_simple))
})

