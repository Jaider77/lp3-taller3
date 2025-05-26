"""
Script principal para ejecutar la aplicación Flask.
"""
import os
from musica_api import create_app
from dotenv import load_dotenv
import logging
from flask import request
from flask_cors import CORS 


# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,  # Cambia a DEBUG para más detalle
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("api.log"),  # Guarda los logs en un archivo
        logging.StreamHandler()          # También muestra los logs en consola
    ]
)

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()

# Crear la aplicación
app = create_app()

# Habilitar CORS después de crear la app
CORS(app)



# Middleware para registrar cada petición y respuesta
@app.before_request
def log_request_info():
    logging.info(f"Petición: {request.method} {request.path} - Datos: {request.get_json(silent=True)}")

@app.after_request
def log_response_info(response):
    logging.info(f"Respuesta: {response.status} - {response.get_data(as_text=True)[:200]}")
    return response



if __name__ == "__main__":
    # Obtener puerto del ambiente o usar 5000 por defecto
    port = int(os.getenv("PORT", 5000))
    
    # Determinar si se debe usar modo debug
    debug = os.getenv("DEBUG", "False").lower() in ["true", "1", "t"]
    
    # Ejecutar aplicación
    app.run(host="0.0.0.0", port=port, debug=debug)


