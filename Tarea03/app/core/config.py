import os


def _get_env(name: str, default: str) -> str:
    return os.environ.get(name, default).strip()


REDIS_URL = _get_env("REDIS_URL", "redis://localhost:6379/0")
# TTL por defecto: lecturas de ficha de socio son frecuentes en recepción; 5 min equilibra frescura y carga.
CACHE_TTL_CLIENT_SECONDS = int(_get_env("CACHE_TTL_CLIENT_SECONDS", "300"))
