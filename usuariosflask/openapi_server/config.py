from datetime import timedelta

class UsuariosConfig:
    USUARIOS_PORT=8080
    USUARIOS_CONTAINER_NAME="usuarios"
    USUARIOS_BASE_URL=f"http://{USUARIOS_CONTAINER_NAME}:{USUARIOS_PORT}"
    # USUARIOS_BASE_URL=f"http://localhost:{USUARIOS_PORT}"

class ContenidosConfig:
    CONTENIDOS_PORT=8081
    CONTENIDOS_CONTAINER_NAME="contenidos"
    CONTENIDOS_BASE_URL=f"http://{CONTENIDOS_CONTAINER_NAME}:{CONTENIDOS_PORT}"
    # CONTENIDOS_BASE_URL=f"http://localhost:{CONTENIDOS_PORT}"

class VisualizacionesConfig:
    VISUALIZACIONES_PORT=8082
    VISUALIZACIONES_CONTAINER_NAME="visualizaciones_recomendaciones"
    VISUALIZACIONES_BASE_URL=f"http://{VISUALIZACIONES_CONTAINER_NAME}:{VISUALIZACIONES_PORT}"
    # VISUALIZACIONES_BASE_URL=f"http://localhost:{VISUALIZACIONES_PORT}"

class Config:
    USUARIOS = UsuariosConfig
    CONTENIDOS = ContenidosConfig
    VISUALIZACIONES = VisualizacionesConfig

    # General Flask configuration
    SECRET_KEY = 'secret_key'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
