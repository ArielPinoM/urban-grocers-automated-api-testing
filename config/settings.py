"""
Configuración central del framework utilizando variables de entorno.

BASE_URL es obligatoria (se genera dinámicamente en TripleTen y caduca).

Otras variables tienen valores por defecto.
"""

import os

def get_required_env(var_name: str) -> str:
    """
    Obtiene una variable de entorno obligatoria.

    Args:
        var_name: Nombre de la variable de entorno

    Returns:
        Valor de la variable

    Raises:
        EnvironmentError: Si la variable no está definida
    """
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(
            f"❌ La variable de entorno '{var_name}' es obligatoria.\n"
            f"Por favor, pásala al ejecutar pytest:\n"
            f"   Linux/Mac: {var_name}=<valor> pytest\n"
            f"   Windows CMD: set {var_name}=<valor> && pytest\n"
            f"   Windows PowerShell: $env: {var_name}='<valor>'; pytest"
        )
    return value

def get_optional_env(var_name: str, default: str) -> str:
    """
    Obtiene una variable de entorno opcional con valor por defecto.

    Args:
        var_name: Nombre de la variable de entorno
        default: Valor por defecto si no está definida

    Returns:
        Valor de la variable o default
    """
    return os.getenv(var_name, default)


# ============================================
# Variables de entorno obligatorias
# ============================================
BASE_URL = get_required_env("BASE_URL")


# ============================================
# Variables de entorno opcionales
# ============================================
TIMEOUT = int(get_optional_env("TIMEOUT", "10"))
LOG_LEVEL = get_optional_env("LOG_LEVEL", "INFO")
ENVIRONMENT = get_optional_env("ENVIRONMENT", "tripleten")


# ============================================
# Headers por defecto para todas las peticiones
# ============================================
DEFAULT_HEADERS = {
    "Content-Type": "application/json"
}


# ============================================
# Validación adicional
# ============================================
def validate_config():
    """Valida que la configuración sea consistente."""
    if not BASE_URL.startswith(("http://", "https://")):
        raise ValueError(f"BASE_URL debe comenzar con http:// o https://. Actual: {BASE_URL}")
    if TIMEOUT <= 0:
        raise ValueError(f"TIMEOUT debe ser positivo. Actual: {TIMEOUT}")

# Ejecutar validación al importar el módulo
validate_config()