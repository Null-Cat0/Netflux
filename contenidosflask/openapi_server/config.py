from datetime import timedelta

# ip = "localhost"
ip = "0.0.0.0"

class UsuariosConfig:
    USUARIOS_PORT=8080
    USUARIOS_BASE_URL=f"http://{ip}:{USUARIOS_PORT}"

class ContenidosConfig:
    CONTENIDOS_PORT=8081
    CONTENIDOS_BASE_URL=f"http://{ip}:{CONTENIDOS_PORT}"

class VisualizacionesConfig:
    VISUALIZACIONES_PORT=8082
    VISUALIZACIONES_BASE_URL=f"http://{ip}:{VISUALIZACIONES_PORT}"

class Config:
    USUARIOS = UsuariosConfig
    CONTENIDOS = ContenidosConfig
    VISUALIZACIONES = VisualizacionesConfig

    # General Flask configuration
    SECRET_KEY = 'secret_key'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
