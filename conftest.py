"""
Global pytest fixtures for the Urban Grocers API framework.

Provide reusable HTTP clients and authentication helpers for tests.
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
    Session-scoped fixture that yields a `BaseClient` instance.

    Reuses a single HTTP session across all tests for efficiency.
    """
    with BaseClient(
        base_url=BASE_URL,
        default_headers=DEFAULT_HEADERS,
        timeout=TIMEOUT,
    ) as client:
        yield client
    # The HTTP session is closed automatically on context exit.

@pytest.fixture(scope="session")
def user_client(base_client):
    """Session-scoped fixture that provides a `UserClient`."""
    return UserClient(base_client)

@pytest.fixture(scope="session")
def kit_client(base_client):
    """Session-scoped fixture that provides a `KitClient`."""
    return KitClient(base_client)

@pytest.fixture(scope="function")
def registered_user_token(user_client):
    """
    Function-scoped fixture that creates a valid user and yields its auth token.

    Each test receives a fresh, isolated user.
    """
    payload = generate_user_payload(include_optional=False)  # only required fields
    response = user_client.create_user(payload=payload, expected_status=201)
    token = response["authToken"]
    yield token
    # There is no user-deletion endpoint, so no cleanup is performed.
    # The API does not appear to require explicit teardown for created users.