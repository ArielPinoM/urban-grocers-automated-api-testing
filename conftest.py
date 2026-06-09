"""
Fixtures globales de pytest para el framework de Urban Grocers API.

Proporcionan clientes HTTP reutilizables y autenticación.
"""

import pytest
from core.base_client import BaseClient
from api_clients.user_client import UserClient
from api_clients.kit_client import KitClient
from utils.data_generator import generate_user_payload
from config.settings import BASE_URL, TIMEOUT, DEFAULT_HEADERS

@pytest.fixture(scope="session")
def base_client():
    """
    Fixture de sesión que proporciona una instancia de BaseClient.

    Reutiliza la misma sesión HTTP para todas las pruebas (eficiente).
    """
    with BaseClient(
        base_url=BASE_URL,
        default_headers=DEFAULT_HEADERS,
        timeout=TIMEOUT,
    ) as client:
        yield client
    # Al salir del contexto, se cierra la sesión automáticamente

@pytest.fixture(scope="session")
def user_client(base_client):
    """Fixture de sesión que proporciona UserClient."""
    return UserClient(base_client)

@pytest.fixture(scope="session")
def kit_client(base_client):
    """Fixture de sesión que proporciona KitClient."""
    return KitClient(base_client)

@pytest.fixture(scope="function")
def registered_user_token(user_client):
    """
    Fixture de función que crea un usuario válido y retorna su token de autenticación.

    Cada prueba recibe un usuario fresco y aislado.
    """
    payload = generate_user_payload(include_optional=False) # Solo campos requeridos
    response = user_client.create_user(payload=payload, expected_status=201)
    token = response["authToken"]
    yield token
    # No hay endpoint de eliminación de usuarios, por lo que no se realiza limpieza.
    # La API de Urban Grocers no parece requerir cleanup explícito.