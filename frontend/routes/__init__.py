from .perfil_routes import perfil_bp
from .usuario_routes import usuario_bp
from .dispositivos_routes import dispositivos_bp
from .contenidos_routes import contenidos_bp

blueprints = [
    perfil_bp,
    usuario_bp,
    dispositivos_bp,
    contenidos_bp
]
