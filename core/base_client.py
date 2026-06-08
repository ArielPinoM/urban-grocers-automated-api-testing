"""
Cliente base HTTP para consumir APIs Rest.
Proporciona funcionalidad común para todas las peticiones HTTP.
"""

import requests
import logging
from typing import Optional, Dict, Any

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseClient:
    """
    Cliente base abstracto para peticiones HTTP

    Maneja sesiones, headers, logging y respuestas de forma centralizada
    """

    def __init__(
            self,
            base_url: str,
            default_headers: Optional[Dict[str, str]] = None,
            session: Optional[requests.Session] = None,
            timeout: int = 10
    ):
        """
        Inicializa el cliente base

        Args:
            base_url (str): URL base de la API
            default_headers (Optional[Dict[str, str]]): Header por defecto para todas las peticiones
            session (Optional[requests.Session]): Sesión de requests reutilizable (opcional)
            timeout (int): Timeout en segundos para las peticiones (default: 10)
        """
        self.base_url = base_url.rstrip('/')
        self.default_headers = default_headers or {
            "Content-Type": "application/json"
        }
        self.timeout = timeout

        # Usar sesión proporcionada o crear una nueva
        if session:
            self.session = session
        else:
            self.session = requests.Session()
            self.session.headers.update(self.default_headers)

    def _build_url(self, endpoint: str) -> str:
        """
        Construye la URL completa a partir del endpoint

        Args:
            endpoint (str): Endpoint de la API

        Returns:
            str: URL completa (base_url + endpoint)
        """
        return f'{self.base_url}/{endpoint.lstrip('/')}'

    @staticmethod
    def _handle_response(response: requests.Response, expected_status: int) -> Dict[str, Any]:
        """
        Procesa la respuesta HTTP, valida el código de estado y retorna el JSON

        Args:
            response: Objeto Response de requests
            expected_status: Código de estado HTTP esperado

        Returns:
            Dict: Diccionario con el cuerpo de la respuesta (JSON)

        Raises:
            AssertionError: Si el código de estado no coincide con el esperado
            requests.exceptions.JSONDecodeError: Si la respuesta no es JSON válido
        """
        status_code = response.status_code
        logger.info(f'Response status: {status_code} (expected: {expected_status})')
        logger.debug(f'Response body: {response.text}')

        # Validar código de estado
        assert status_code == expected_status, \
            f'Expected status {expected_status}, but got {status_code}. Response: {response.text}'

        # Intentar parsear JSON
        if response.text:
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                logger.warning(f'Response is not valid JSON: {response.text}')
                return {"raw_response": response.text}
        return {}

    def _request(
            self,
            method: str,
            endpoint: str,
            expected_status: int = 200,
            headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> Dict[str, Any]:
        """
        Método interno para realizar peticiones HTTP

        Args:
            method: Método HTTP (GET, POST, PUT, DELETE, etc.)
            endpoint: Endpoint de la API
            expected_status: Código de estado esperado (default: 200)
            headers: Headers adicionales para esta petición
            params: Parámetros de query string
            data: Datos para enviar en formato form-data
            json: Datos para enviar en formato json
            **kwargs: Argumentos adicionales para requests

        Returns: Diccionario con la respuesta parseada
        """
        url = self._build_url(endpoint=endpoint)
        request_headers = self.default_headers.copy()

        if headers:
            request_headers.update(headers)

        logger.info(f'Making {method} request to: {url}')
        logger.debug(f'Headers: {request_headers}')
        logger.debug(f'Params: {params}')
        logger.debug(f'Data/JSON: {data or json}')

        response = self.session.request(
            method=method,
            url=url,
            headers=request_headers,
            params=params,
            data=data,
            json=json,
            timeout=self.timeout,
            **kwargs
        )

        return self._handle_response(response=response, expected_status=expected_status)

    def get(
            self,
            endpoint: str,
            expected_status: int = 200,
            headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> Dict[str, Any]:
        """
        Realiza una petición GET

        Args:
            endpoint: Endpoint de la API
            expected_status: Código de estado esperado
            headers: Headers adicionales
            params: Parámetros de query string
            **kwargs: Argumentos adicionales

        Returns:
            Diccionario con la respuesta
        """
        return self._request(method="GET", endpoint=endpoint, expected_status=expected_status, headers=headers, params=params, **kwargs)

    def post(
            self,
            endpoint: str,
            expected_status: int = 201,
            headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> Dict[str, Any]:
        """
        Realiza una petición POST

        Args:
            endpoint: Endpoint de la API
            expected_status: Código de estado esperado (default: 201)
            headers: Header adicionales
            params: Parámetros de query string
            data: Datos form-data
            json: Datos JSON
            **kwargs: Argumentos adicionales

        Returns:
            Diccionario con la respuesta
        """
        return self._request("POST", endpoint=endpoint, expected_status=expected_status, headers=headers, params=params, data=data, json=json, **kwargs)

    # Pendiente función put

    # Pendiente función delete

    def close(self):
        """Cierra la sesión HTTP"""
        self.session.close()

    def __enter__(self):
        """Soporte para context manager (with statement)"""
        return self

    def __exit__(self):
        """Cierra la sesión al salir del context manager"""
        self.close()