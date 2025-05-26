import os

class Config:
    # Seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-default-123'

    # Rutas estáticas
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Otras configuraciones (para expandir en el futuro)
    DEBUG = True
    TESTING = False
    ENV = 'development'
