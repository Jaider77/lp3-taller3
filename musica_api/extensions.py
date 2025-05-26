"""
Módulo de extensiones para la aplicación Flask.
Define las instancias de las extensiones utilizadas en todo el proyecto.
"""
from flask_sqlalchemy import SQLAlchemy 
from flask_restx import Api

# API RESTful con documentación Swagger integrada
api = Api(
    title="API de Música",
    version="1.0",
    description="API para gestionar Usuarios, Canciones y Favoritos",
    doc="/docs"
)

# ORM para interactuar con la base de datos
db = SQLAlchemy()
