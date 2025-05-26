"""
Módulo de configuración de la aplicación.
Define las diferentes configuraciones para entornos de desarrollo, pruebas y producción.
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()

class Config:
    """Configuración base para la aplicación."""
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite://Users/Admin/Public/musica.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() == 'true'
    API_TITLE = os.getenv('API_TITLE', 'API de Música')
    API_VERSION = os.getenv('API_VERSION', '1.0')
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-secreta-predeterminada')
    
    # Configuración de la API
    API_TITLE = os.getenv('API_TITLE', 'API de Música')
    API_VERSION = os.getenv('API_VERSION', '1.0')
    
    # Otras configuraciones generales
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-secreta-predeterminada')

class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo."""
    DEBUG = True
    
class TestingConfig(Config):
    """Configuración para entorno de pruebas."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///musica_test.db'
    
class ProductionConfig(Config):
    """Configuración para entorno de producción."""
    DEBUG = False
    # En producción, asegurarse de tener una clave secreta fuerte
    SECRET_KEY = os.getenv('SECRET_KEY')
    
# Mapeo de configuraciones por entorno
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Obtener configuración según el entorno
def get_config(env=None):
    """
    Obtiene la configuración según el entorno especificado en las variables de entorno o argumento.
    
    Args:
        env (str): Nombre del entorno ('development', 'testing', 'production', etc.)
    Returns:
        object: Clase de configuración según el entorno.
    """
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, config_by_name['default'])
