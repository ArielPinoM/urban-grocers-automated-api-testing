"""
Cliente para interactuar con el endpoint de kits de Urban Grocers API.

Maneja la creación de kits asociados a un usuario (vía token) o a una tarjeta.
"""

from core.base_client import BaseClient
from typing import Optional


class KitClient(BaseClient):
    """
    Cliente específico para operaciones del endpoint /api/v1/kits.

    Hereda de BaseClient para reutilizar lógica HTTP.
    """

    def __init__(self, base_client: BaseClient):
        """
        Inicializa KitClient con una instancia de BaseClient.

        Args:
             base_client: Instancia configurada de BaseClient (URL base, headers, session)
        """
        super().__init__(
            base_url=base_client.base_url,
            default_headers=base_client.default_headers,
            session=base_client.session
        )

    def create_kit(
            self,
            name: str,
            auth_token: Optional[str] = None,
            card_id: Optional[int] = None,
            expected_status: int = 201
    ) -> dict:
        """
        Crea un kit personal para un usuario o tarjeta.

        Args:
            name: Nombre del kit (string, validaciones: 2-15 caracteres, letras latinas, espacio, guión)
            auth_token: Token de autenticación (Bearer). Si se proporciona, tiene prioridad sobre card_id
            card_id: ID de la tarjeta (opcional, usado solo si no hay auth_token)
            expected_status: Código de estado HTTP esperado (default: 201)

        Returns:
            Diccionario con la respuesta de la API
            Éxito: {"name": str, "card: {...}, "id": int, "productsList": None, "productsCount": 0}
            Error: {"code": 400, "message": str}

        Raises:
            AssertionError: Si el código de estado recibido no coincide con expected_status
        """
        headers = {}
        if auth_token:
            headers["Authorization"] = f'Bearer {auth_token}'

        params = {}
        if card_id is not None and not auth_token:
            params["cardId"] = card_id

        payload = {"name": name}

        return self.post(
            endpoint="/api/v1/kits",
            json=payload,
            headers=headers if headers else None,
            params=params if params else None,
            expected_status=expected_status
        )

    def create_kit_with_raw_payload(
            self,
            payload: dict,
            auth_token: Optional[str] = None,
            card_id: Optional[int] = None,
            expected_status: int = 201
    ) -> dict:
        """
        Crea un kit enviando un payload arbitrario (útil para pruebas de validación).

        Args:
            payload: Diccionario con los datos a enviar (ej. {"name": 123} o {})
            auth_token: Token de autenticación (Bearer)
            card_id: ID de la tarjeta (opcional)
            expected_status: Código de estado HTTP esperado

        Returns:
            Respuesta de la API
        """
        headers = {}
        if auth_token:
            headers["Authorization"] = f'Bearer {auth_token}'

        params = {}
        if card_id is not None and not auth_token:
            params["cardId"] = card_id

        return self.post(
            endpoint="/api/v1/kits",
            json=payload,
            headers=headers if headers else None,
            params=params if params else None,
            expected_status=expected_status
        )