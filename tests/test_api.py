"""
Módulo de pruebas para la API.
Contiene pruebas unitarias y de integración para verificar el funcionamiento correcto de la API.
"""
import unittest
import json
from musica_api import create_app
from musica_api.extensions import db
from musica_api.models import Usuario, Cancion, Favorito

class TestAPI(unittest.TestCase):
    """Clase base para las pruebas de la API."""
    
    def setUp(self):
        """Prepara el entorno de prueba antes de cada test."""
        # Configurar la aplicación para pruebas
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        # Crear un cliente de prueba
        self.client = self.app.test_client()
        
        # Crear contexto de aplicación
        with self.app.app_context():
            db.create_all()
            self._crear_datos_prueba()
    
    def tearDown(self):
        """Limpia el entorno después de cada test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def _crear_datos_prueba(self):
        """Crea datos de prueba en la base de datos."""
        # Crear usuarios
        usuario1 = Usuario(nombre="Usuario Test 1", correo="usuario1@test.com")
        usuario2 = Usuario(nombre="Usuario Test 2", correo="usuario2@test.com")
        
        # Crear canciones
        cancion1 = Cancion(
            titulo="Canción Test 1",
            artista="Artista Test 1",
            album="Album Test 1",
            duracion=180,
            año=2020,
            genero="Rock"
        )
        cancion2 = Cancion(
            titulo="Canción Test 2",
            artista="Artista Test 2",
            album="Album Test 2",
            duracion=240,
            año=2021,
            genero="Pop"
        )
        
        # Agregar a la base de datos
        db.session.add_all([usuario1, usuario2, cancion1, cancion2])
        db.session.commit()
        
        # Crear favorito
        favorito = Favorito(id_usuario=usuario1.id, id_cancion=cancion1.id)
        db.session.add(favorito)
        db.session.commit()

class TestUsuarios(TestAPI):
    """Pruebas para los endpoints de usuarios."""
    
    def test_listar_usuarios(self):
        """Prueba el endpoint para listar usuarios."""
        response = self.client.get('/api/usuarios')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
    
    def test_obtener_usuario(self):
        """Prueba el endpoint para obtener un usuario por ID."""
        response = self.client.get('/api/usuarios/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['nombre'], "Usuario Test 1")
        self.assertEqual(data['correo'], "usuario1@test.com")
    
    def test_crear_usuario(self):
        """Prueba el endpoint para crear un usuario."""
        nuevo_usuario = {
            "nombre": "Usuario Nuevo",
            "correo": "nuevo@test.com"
        }
        response = self.client.post(
            '/api/usuarios',
            data=json.dumps(nuevo_usuario),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['nombre'], "Usuario Nuevo")
        
        # Verificar que se ha creado en la base de datos
        response = self.client.get('/api/usuarios/3')
        self.assertEqual(response.status_code, 200)

class TestCanciones(TestAPI):
    """Pruebas para los endpoints de canciones."""
    
    def test_listar_canciones(self):
        """Prueba el endpoint para listar canciones."""
        response = self.client.get('/api/canciones')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
    
    def test_buscar_canciones(self):
        """Prueba el endpoint para buscar canciones."""
        response = self.client.get('/api/canciones/buscar?genero=Rock')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['titulo'], "Canción Test 1")

class TestFavoritos(TestAPI):
    """Pruebas para los endpoints de favoritos."""
    
    def test_listar_favoritos_usuario(self):
        """Prueba el endpoint para listar favoritos de un usuario."""
        response = self.client.get('/api/usuarios/1/favoritos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['canciones_favoritas']), 1)
        self.assertEqual(data['canciones_favoritas'][0]['titulo'], "Canción Test 1")

if __name__ == '__main__':
    unittest.main()

