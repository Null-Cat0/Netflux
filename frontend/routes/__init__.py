from .perfil_routes import perfil_bp
from .usuario_routes import usuario_bp
from .dispositivos_routes import dispositivos_bp
from .pelicula_routes import pelicula_bp
from .serie_routes import serie_bp
from .actor_routes import actor_bp

blueprints = [
    perfil_bp,
    usuario_bp,
    dispositivos_bp,
    pelicula_bp,
    serie_bp,
    actor_bp,
]
