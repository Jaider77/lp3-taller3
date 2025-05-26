"""
Módulo principal de inicialización de la aplicación Flask.
Configura la aplicación, las extensiones y registra los namespaces.
"""
from flask import Flask
from .extensions import api, db
from .resources import ns
from .config import get_config
import os

def create_app(config_name=None):
    """
    Crea y configura la aplicación Flask con sus extensiones.
    
    Args:
        config_name (str): Nombre de la configuración a utilizar (default, development, testing, production).
                          Si es None, se utiliza la configuración según las variables de entorno.
    
    Returns:
        Flask: La aplicación Flask configurada y lista para usar.
    """
    ## Crear la app Flask
    app = Flask(__name__)
    
    # Aplicar configuración según entorno
    config_obj = get_config(config_name or os.getenv("FLASK_ENV", "default"))
    app.config.from_object(config_obj)
    
    # Inicialización de extensiones
    db.init_app(app)
    api.init_app(app)
    
    # Registro de namespaces
    api.add_namespace(ns, path='/api')
    
    # Crear todas las tablas en la base de datos
    with app.app_context():
        db.create_all()
    
    return app

