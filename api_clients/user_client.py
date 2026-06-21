"""
Cliente para interactuar con el endpoint de usuarios de Urban Grocers API.
Maneja la creación de usuarios y obtención de tokens de autenticación.
"""
from typing import Optional

from core.base_client import BaseClient


class UserClient(BaseClient):
    """
    Cliente específico para operaciones del endpoint /api/v1/users.

    Hereda de BaseClient para reutilizar lógica HTTP.
    """

    def __init__(self, base_client: BaseClient):
        """
        Inicializa UserClient con una instancia de BaseClient.

        Args:
            base_client: Instancia configurada de BaseClient (URL base, headers, session)
        """
        super().__init__(
            base_url=base_client.base_url,
            default_headers=base_client.default_headers,
            session=base_client.session
        )

    def create_user(self, payload: dict, expected_status: int = 201) -> dict:
        """
        Crea un nuevo usuario en el sistema.

        Args:
            payload: Diccionario con los datos del usuario.
                Mínimo requerido: firstName, phone, address.
                Opcional: email, comment.
            expected_status: Código de estado HTTP esperado (default: 201).

        Returns:
            Diccionario con la respuesta de la API.
            En caso exitoso: {"authToken": "token_string"}
            En caso de error: {"code": 400, "message": "..."}

        Raises:
            AssertionError: Si el código de estado recibido no coincide con expected_status.
        """
        response = self.post(
            endpoint="/api/v1/users",
            json=payload,
            expected_status=expected_status
        )
        return response

    def create_user_minimal(self, first_name: str, phone: str, address: str, expected_status: int = 201) -> dict:
        """
        Crea un usuario con el conjunto mínimo de datos requeridos.

        Args:
            first_name: Nombre del usuario (solo letras latinas, 2-15 caracteres)
            phone: Número de teléfono (solo números y signo +)
            address: Dirección (caracteres latinos y puntuación, 5-50 caracteres)
            expected_status: Código de estado HTTP esperado

        Returns:
            Diccionario con la respuesta de la API.
        """
        payload = {
            "firstName": first_name,
            "phone": phone,
            "address": address,
        }
        return self.create_user(payload, expected_status)

    def create_user_complete(
            self,
            first_name: str,
            phone: str,
            address: str,
            email: Optional[str] = None,
            comment: Optional[str] = None,
            expected_status: int = 201
    ) -> dict:
        """
        Crea un usuario con información completa (campos opcionales incluidos)

        Args:
            first_name: Nombre del usuario
            phone: Número de teléfono
            address: Dirección
            email: Correo electrónico (opcional)
            comment: Comentario adicional (opcional)
            expected_status: Código de estado HTTP esperado

        Returns:
            Diccionario con la respuesta de la API
        """
        payload = {
            "firstName": first_name,
            "phone": phone,
            "address": address,
        }
        if email:
            payload["email"] = email
        if comment:
            payload["comment"] = comment

        return self.create_user(payload, expected_status)

    @staticmethod
    def get_auth_token_from_response(response: dict) -> str:
        """
        Extrae el token de autenticación de la respuesta de creación de usuario.

        Args:
            response: Respuesta de la API (diccionario)

        Returns:
            Token de autenticación como string

        Raises:
            KeyError: Si el token no está presente en la respuesta
        """
        return response["authToken"]