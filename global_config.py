from datetime import timedelta

class UsuariosConfig:
    USUARIOS_PORT=8080
    USUARIOS_BASE_URL=f"http://localhost:{USUARIOS_PORT}"

class ContenidosConfig:
    CONTENIDOS_PORT=8081
    CONTENIDOS_BASE_URL=f"http://localhost:{CONTENIDOS_PORT}"

class VisualizacionesConfig:
    VISUALIZACIONES_PORT=8082
    VISUALIZACIONES_BASE_URL=f"http://localhost:{VISUALIZACIONES_PORT}"

class Config:
    USUARIOS = UsuariosConfig
    CONTENIDOS = ContenidosConfig
    VISUALIZACIONES = VisualizacionesConfig

    # General Flask configuration
    SECRET_KEY = 'secret_key'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
