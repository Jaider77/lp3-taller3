"""
Módulo de recursos de la API.
Define los endpoints, controladores y la lógica de negocio de la API.
"""
import logging
from flask import request
from flask_restx import Resource, Namespace
from werkzeug.security import generate_password_hash, check_password_hash
from .api_models import (
    usuario_model, usuario_base, 
    cancion_model, cancion_base,
    favorito_model, favorito_input, 
    favoritos_usuario_model, mensaje_model
)
from .extensions import db
from .models import Usuario, Cancion, Favorito

# Namespace para agrupar los recursos de la API
ns = Namespace("api", description="Operaciones de la API de música")

# Recurso para probar la API
@ns.route("/ping")
class Ping(Resource):
    @ns.response(200, "API funcionando correctamente")
    @ns.marshal_with(mensaje_model)
    def get(self):
        """Endpoint para verificar que la API está funcionando"""
        return {"mensaje": "API funcionando correctamente"}, 200

# Recursos para Usuarios

@ns.route("/usuarios")
class UsuarioListAPI(Resource):
    @ns.marshal_list_with(usuario_model)
    def get(self):
        """Devuelve la lista de todos los usuarios"""
        return Usuario.query.all(), 200

    @ns.doc("Crear un nuevo usuario")
    @ns.expect(usuario_base)
    @ns.response(201, "Usuario creado con éxito")
    @ns.response(400, "Datos inválidos o correo ya existe")
    @ns.marshal_with(usuario_model)
    def post(self):
        data = request.json
        logging.info(f"Intentando crear usuario con datos: {data}")  # <-- Logging de intento

        # Verificar si el correo ya existe
        if Usuario.query.filter_by(correo=data["correo"]).first():
            logging.warning(f"Intento de registro con correo ya existente: {data['correo']}")  # <-- Logging de advertencia
            ns.abort(400, "El correo electrónico ya está registrado")
        # Hash de la contraseña
        contrasena_hash = generate_password_hash(data["contrasena"])
        
        usuario = Usuario(
            nombre=data["nombre"],
            correo=data["correo"],
            contrasena=contrasena_hash
        )

        try:
            db.session.add(usuario)
            db.session.commit()
            logging.info(f"Usuario creado exitosamente: {usuario.id}")  # <-- Logging de éxito
            return usuario, 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error al crear usuario: {str(e)}")  # <-- Logging de error
            ns.abort(400, f"Error al crear usuario: {str(e)}")

@ns.route("/login")
class LoginAPI(Resource):
    @ns.doc("Iniciar sesión de usuario")
    def post(self):
        data = request.json
        correo = data.get("correo")
        contrasena = data.get("contrasena")
        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario and check_password_hash(usuario.contrasena, contrasena):
            es_admin = usuario.correo.endswith("@admin.com")
            return {
                "success": True,
                "mensaje": "Inicio de sesión exitoso",
                "usuario_id": usuario.id,
                "admin": es_admin
            }
        else:
            return {"success": False, "mensaje": "Correo o contraseña incorrectos"}, 401

@ns.route("/usuarios/<int:id>")
@ns.param("id", "Identificador único del usuario")
@ns.response(404, "Usuario no encontrado")
class UsuarioAPI(Resource):
    @ns.doc("Obtener un usuario por su ID")
    @ns.marshal_with(usuario_model)
    def get(self, id):
        """Obtiene un usuario por su ID"""
        return Usuario.query.get_or_404(id)

    @ns.doc("Actualizar un usuario")
    @ns.expect(usuario_base)
    @ns.marshal_with(usuario_model)
    def put(self, id):
        """Actualiza un usuario existente"""
        usuario = Usuario.query.get_or_404(id)
        data = request.json
        
        # Verificar si se intenta cambiar el correo a uno ya existente
        if "correo" in data and data["correo"] != usuario.correo:
            if Usuario.query.filter_by(correo=data["correo"]).first():
                ns.abort(400, "El correo electrónico ya está registrado")
        
        usuario.nombre = data.get("nombre", usuario.nombre)
        usuario.correo = data.get("correo", usuario.correo)
        
        try:
            db.session.commit()
            return usuario
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al actualizar usuario: {str(e)}")
    
    @ns.doc("Eliminar un usuario")
    @ns.response(204, "Usuario eliminado con éxito")
    def delete(self, id):
        """Elimina un usuario existente"""
        usuario = Usuario.query.get_or_404(id)
        try:
            db.session.delete(usuario)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al eliminar usuario: {str(e)}")

# Recursos para Canciones
@ns.route("/canciones")
class CancionListAPI(Resource):
    @ns.doc("Listar todas las canciones")
    @ns.response(200, "Lista de canciones obtenida con éxito")
    @ns.marshal_list_with(cancion_model)
    def get(self):
        """Obtiene todas las canciones registradas"""
        return Cancion.query.all(), 200

    @ns.doc("Crear una nueva canción")
    @ns.expect(cancion_base)
    @ns.response(201, "Canción creada con éxito")
    @ns.marshal_with(cancion_model)
    def post(self):
        """Crea una nueva canción"""
        data = request.json
        logging.info(f"Intentando crear usuario con datos: {data}")
        
        cancion = Cancion(
            titulo=data["titulo"],
            artista=data["artista"],
            album=data.get("album"),
            duracion=data.get("duracion"),
            año=data.get("año"),
            genero=data.get("genero")
        )
        
        try:
            db.session.add(cancion)
            db.session.commit()
            return cancion, 201
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al crear canción: {str(e)}")

@ns.route("/canciones/<int:id>")
@ns.param("id", "Identificador único de la canción")
@ns.response(404, "Canción no encontrada")
class CancionAPI(Resource):
    @ns.doc("Obtener una canción por su ID")
    @ns.marshal_with(cancion_model)
    def get(self, id):
        """Obtiene una canción por su ID"""
        return Cancion.query.get_or_404(id)

    @ns.doc("Actualizar una canción")
    @ns.expect(cancion_base)
    @ns.marshal_with(cancion_model)
    def put(self, id):
        """Actualiza una canción existente"""
        cancion = Cancion.query.get_or_404(id)
        data = request.json
        
        cancion.titulo = data.get("titulo", cancion.titulo)
        cancion.artista = data.get("artista", cancion.artista)
        cancion.album = data.get("album", cancion.album)
        cancion.duracion = data.get("duracion", cancion.duracion)
        cancion.año = data.get("año", cancion.año)
        cancion.genero = data.get("genero", cancion.genero)
        
        try:
            db.session.commit()
            return cancion
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al actualizar canción: {str(e)}")
    
    @ns.doc("Eliminar una canción")
    @ns.response(204, "Canción eliminada con éxito")
    def delete(self, id):
        """Elimina una canción existente"""
        cancion = Cancion.query.get_or_404(id)
        try:
            db.session.delete(cancion)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al eliminar canción: {str(e)}")

# Recursos para buscar canciones
@ns.route("/canciones/buscar")
class CancionBusquedaAPI(Resource):
    @ns.doc("Buscar canciones por título, artista o género")
    @ns.param("titulo", "Título de la canción (búsqueda parcial)")
    @ns.param("artista", "Nombre del artista (búsqueda parcial)")
    @ns.param("genero", "Género musical (búsqueda exacta)")
    @ns.marshal_list_with(cancion_model)
    def get(self):
        """Busca canciones por título, artista o género"""
        titulo = request.args.get("titulo")
        artista = request.args.get("artista")
        genero = request.args.get("genero")
        
        query = Cancion.query
        
        if titulo:
            query = query.filter(Cancion.titulo.ilike(f"%{titulo}%"))
        if artista:
            query = query.filter(Cancion.artista.ilike(f"%{artista}%"))
        if genero:
            query = query.filter(Cancion.genero == genero)
            
        return query.all()

# Recursos para Favoritos
@ns.route("/favoritos")
class FavoritoListAPI(Resource):
    @ns.doc("Listar todos los favoritos")
    @ns.response(200, "Lista de favoritos obtenida con éxito")
    @ns.marshal_list_with(favorito_model)
    def get(self):
        """Obtiene todos los registros de favoritos"""
        return Favorito.query.all(), 200
    
    @ns.doc("Marcar una canción como favorita")
    @ns.expect(favorito_input)
    @ns.response(201, "Canción marcada como favorita")
    @ns.response(400, "Datos inválidos o relación ya existe")
    @ns.response(404, "Usuario o canción no encontrada")
    @ns.marshal_with(favorito_model)
    def post(self):
        """Marca una canción como favorita para un usuario"""
        data = request.json
        
        # Verificar si existen el usuario y la canción
        usuario = Usuario.query.get(data["id_usuario"])
        cancion = Cancion.query.get(data["id_cancion"])
        
        if not usuario:
            ns.abort(404, "Usuario no encontrado")
        if not cancion:
            ns.abort(404, "Canción no encontrada")
        
        # Verificar si ya existe el favorito
        favorito_existente = Favorito.query.filter_by(
            id_usuario=data["id_usuario"],
            id_cancion=data["id_cancion"]
        ).first()
        
        if favorito_existente:
            ns.abort(400, "La canción ya está marcada como favorita para este usuario")
        
        favorito = Favorito(
            id_usuario=data["id_usuario"],
            id_cancion=data["id_cancion"]
        )
        
        try:
            db.session.add(favorito)
            db.session.commit()
            return favorito, 201
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al marcar canción como favorita: {str(e)}")

@ns.route("/favoritos/usuario/<int:id_usuario>")
@ns.param("id_usuario", "Identificador del usuario")
class FavoritosUsuarioAPI(Resource):
    @ns.doc("Listar las canciones favoritas de un usuario")
    @ns.response(200, "Lista de favoritos obtenida con éxito")
    @ns.marshal_with(favoritos_usuario_model)
    def get(self, id_usuario):
        """Obtiene las canciones favoritas de un usuario"""
        usuario = Usuario.query.get_or_404(id_usuario)
        favoritos = Favorito.query.filter_by(id_usuario=id_usuario).all()
        return favoritos, 200
