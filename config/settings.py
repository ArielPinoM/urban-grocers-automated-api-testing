"""
Central configuration for the test framework using environment variables.

`BASE_URL` is required (it is generated dynamically by TripleTen and expires).
Other settings have sensible defaults.
"""

import os

def get_required_env(var_name: str) -> str:
    """
    Retrieve a required environment variable.

    Args:
        var_name: Environment variable name

    Returns:
        The variable value

    Raises:
        EnvironmentError: if the variable is not set
    """
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(
            f"❌ The environment variable '{var_name}' is required.\n"
            f"Please pass it when running pytest:\n"
            f"   Linux/Mac: {var_name}=<value> pytest\n"
            f"   Windows CMD: set {var_name}=<value> && pytest\n"
            f"   Windows PowerShell: $env:{var_name}='<value>'; pytest\n"
        )
    return value

def get_optional_env(var_name: str, default: str) -> str:
    """
    Retrieve an optional environment variable with a default value.

    Args:
        var_name: Environment variable name
        default: Default value if not set

    Returns:
        The variable value or the provided default
    """
    return os.getenv(var_name, default)


# ============================================
# Required environment variables
# ============================================
BASE_URL = get_required_env("BASE_URL")


# ============================================
# Optional environment variables
# ============================================
TIMEOUT = int(get_optional_env("TIMEOUT", "10"))
LOG_LEVEL = get_optional_env("LOG_LEVEL", "INFO")
ENVIRONMENT = get_optional_env("ENVIRONMENT", "tripleten")


# ============================================
# Default headers for all requests
# ============================================
DEFAULT_HEADERS = {
    "Content-Type": "application/json"
}


# ============================================
# Additional validation
# ============================================
def validate_config():
    """Validate that configuration values are consistent."""
    if not BASE_URL.startswith(("http://", "https://")):
        raise ValueError(f"BASE_URL must start with http:// or https://. Actual: {BASE_URL}")
    if TIMEOUT <= 0:
        raise ValueError(f"TIMEOUT must be positive. Actual: {TIMEOUT}")


# Run validation on import
validate_config()