# Datos del estudiante
Nombre: Jaider Francisco Asprilla Reyes
CC:1077631902
### Registro (logging)

La API implementa un sistema de registro que guarda eventos importantes y errores en el archivo `api.log`. Esto permite monitorear el uso y detectar problemas rápidamente.  
Cada petición y respuesta HTTP queda registrada, incluyendo los datos enviados y recibidos.

# API de Música

Una [API RESTful](https://aws.amazon.com/es/what-is/restful-api/) para gestionar usuarios, canciones y relaciones de favoritos. Desarrollada con [Flask](https://flask.palletsprojects.com/en/stable/), [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/), [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/) y [SQLAlchemy](https://www.sqlalchemy.org/).

## Descripción

Esta API permite administrar:
- **Usuarios**: crear y gestionar perfiles de usuarios.
- **Canciones**: agregar, actualizar y eliminar canciones con sus metadatos.
- **Favoritos**: gestionar las canciones favoritas de cada usuario.

El proyecto incluye una interfaz de documentación interactiva generada automáticamente con [Swagger](https://swagger.io/) disponible en el *endpoint* `/docs`.

## Estructura del Proyecto

```
lp3-taller2
├──  README.md            # Este archivo, documentación completa del proyecto
├──  .env                 # Variables de entorno (desarrollo, pruebas, producción)
├──  .gitignore           # Archivos y directorios a ignorar por Git
├──  app.py               # Script principal para ejecutar la aplicación
├──  instance
│   └──  musica.db        # Base de Datos
├──  musica_api
│   ├──  __init__.py      # Inicialización del módulo
│   ├──  api_models.py    # Modelos de API para serialización/deserialización usando Flask-RESTX
│   ├──  config.py        # Configuraciones para diferentes entornos (desarrollo, pruebas, producción)
│   ├──  extensions.py    # Definición de Extensiones Flask (API, SQLAlchemy)
│   ├──  models.py        # Modelos de datos usando SQLAlchemy
│   └──  resources.py     # Recursos y endpoints de la API
├── 󰌠 requirements.txt     # Dependencias del proyecto
├── 󰙨 tests
│   └──  test_api.py      # Pruebas Unitarias
└──  utils.py             # Funciones de utilidad

```
## Modelo de Datos

1. **Usuario**:
   - id: Identificador único
   - nombre: Nombre del usuario
   - correo: Correo electrónico (único)
   - fecha_registro: Fecha de registro

2. **Canción**:
   - id: Identificador único
   - titulo: Título de la canción
   - artista: Artista o intérprete
   - album: Álbum al que pertenece
   - duracion: Duración en segundos
   - año: Año de lanzamiento
   - genero: Género musical
   - fecha_creacion: Fecha de creación del registro

3. **Favorito**:
   - id: Identificador único
   - id_usuario: ID del usuario (clave foránea)
   - id_cancion: ID de la canción (clave foránea)
   - fecha_marcado: Fecha en que se marcó como favorito

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/UR-CC/lp3-taller2.git
   cd lp3-taller2
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ajusta las variables de entorno, editando el archivo `.env`

## Ejecución

1. Ejecuta la aplicación:

   ```bash
   flask run
   ```

2. Accede a la aplicación:
   - API: [http://127.0.0.1:5000/api/](http://127.0.0.1:5000/api/)
   - Documentación *Swagger*: [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)

## Uso de la API

### Usuarios

- **Listar usuarios**: `GET /api/usuarios`
- **Crear usuario**: `POST /api/usuarios`
- **Obtener usuario**: `GET /api/usuarios/{id}`
- **Actualizar usuario**: `PUT /api/usuarios/{id}`
- **Eliminar usuario**: `DELETE /api/usuarios/{id}`

### Canciones

- **Listar canciones**: `GET /api/canciones`
- **Crear canción**: `POST /api/canciones`
- **Obtener canción**: `GET /api/canciones/{id}`
- **Actualizar canción**: `PUT /api/canciones/{id}`
- **Eliminar canción**: `DELETE /api/canciones/{id}`
- **Buscar canciones**: `GET /api/canciones/buscar?titulo=value&artista=value&genero=value`

### Favoritos

- **Listar favoritos**: `GET /api/favoritos`
- **Marcar favorito**: `POST /api/favoritos`
- **Obtener favorito**: `GET /api/favoritos/{id}`
- **Eliminar favorito**: `DELETE /api/favoritos/{id}`
- **Listar favoritos de usuario**: `GET /api/usuarios/{id}/favoritos`
- **Marcar favorito específico**: `POST /api/usuarios/{id_usuario}/favoritos/{id_cancion}`
- **Eliminar favorito específico**: `DELETE /api/usuarios/{id_usuario}/favoritos/{id_cancion}`

## Desarrollo del Taller

1. Ajustar este `README.md` con los datos del Estudiante

2. Utilizando [DBeaver](https://dbeaver.io/), adiciona 5 usuarios y 10 canciones, directo a las tablas.

3. Busca todos los comentarios `# TODO`, realiza los ajustes necesarios, y ejecuta un `commit` por cada uno.

4. Prueba el funcionamiento del API, desde la documentación *Swagger*.

5. Implementar una (1) de las sugerencias que se presentan a continuación.

## Sugerencias de Mejora

1. **Autenticación y autorización**: Implementar JWT o OAuth2 para proteger los endpoints y asociar los usuarios automáticamente con sus favoritos.

2. **Paginación**: Añadir soporte para paginación en las listas de canciones, usuarios y favoritos para mejorar el rendimiento con grandes volúmenes de datos.

3. **Validación de datos**: Implementar validación más robusta de datos de entrada utilizando bibliotecas como Marshmallow o Pydantic.

4. **Tests unitarios e integración**: Desarrollar pruebas automatizadas para verificar el funcionamiento correcto de la API.

5. **Base de datos en producción**: Migrar a una base de datos más robusta como PostgreSQL o MySQL para entornos de producción.

6. **Docker**: Contenerizar la aplicación para facilitar su despliegue en diferentes entornos.

7. **Registro (logging)**: Implementar un sistema de registro más completo para monitorear errores y uso de la API.

8. **Caché**: Añadir caché para mejorar la velocidad de respuesta en consultas frecuentes.

9. **Estadísticas de uso**: Implementar un sistema de seguimiento para analizar qué canciones son más populares y sugerir recomendaciones basadas en preferencias similares.

10. **Subida de archivos**: Permitir la subida de archivos de audio y gestionar su almacenamiento en un servicio como S3 o similar.

