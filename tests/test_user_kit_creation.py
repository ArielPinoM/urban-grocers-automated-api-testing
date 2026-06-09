"""
Pruebas automatizadas para la creación de kits de productos en Urban Grocers.

Valida el campo 'name' según la lista de comprobación.
"""

import pytest
from utils.data_generator import generate_kit_name, generate_kit_name_with_special_chars, generate_kit_name_with_spaces


class TestKitCreation:
    """Clase que agrupa todas las pruebas relacionadas con la creación de kits."""
    @pytest.mark.parametrize(
        "kit_name, expected_status, should_check_name",
        [
            # Test 1: 1 carácter (permitido, debe crear kit)
            ("a", 201, True),
            # Test 2: 511 caracteres (permitido, debe crear kit)
            (generate_kit_name(511), 201, True),
            # Test 3: 0 caracteres (no permitido, error 400)
            ("", 400, False),
            # Test 4: 512 caracteres (no permitido, error 400)
            (generate_kit_name(512), 400, False),
            # Test 5: caracteres especiales (permitido, debe crear kit)
            (generate_kit_name_with_special_chars(5), 201, True),
            # Test 6: espacios (permitido, debe crear kit)
            (generate_kit_name_with_spaces(6), 201, True),
            # Test 7: solo números (permitido, debe crear kit)
            ("123", 201, True),
            # Test 8: parámetro 'name' ausente (payload vacío, error 400)
            (None, 400, False)
        ],
        ids=[
            "1_char",
            "511_chars",
            "0_chars",
            "512_chars",
            "special_chars",
            "spaces",
            "numbers",
            "missing_name"
        ]
    )
    def test_kit_name_validation(
            self,
            kit_client,
            registered_user_token,
            kit_name,
            expected_status,
            should_check_name
    ):
        """
        Prueba parametrizada que valida el campo 'name' en creación de kits.
        """
        # Construir payload según sea el caso
        if kit_name is None:
            payload = {}
        else:
            payload = {"name": kit_name}

        # Enviar solicitud usando el método que acepta payload crudo
        response = kit_client.create_kit_with_raw_payload(
            payload=payload,
            auth_token=registered_user_token,
            expected_status=expected_status
        )

        # Verificar que el nombre coincide si la creación fue exitosa y se espera coincidencia
        if expected_status == 201 and should_check_name and kit_name is not None:
            assert response["name"] == kit_name, \
            f"En nombre en la respuesta ({response["name"]}) no coincide con el enviado ({kit_name})"

    def test_kit_name_with_integer_type(self, kit_client, registered_user_token):
        """
        Test 9: Se pasa un número en lugar de string como valor de 'name'.

        La API debe responder con error 400.
        """
        payload = {"name": 123}
        kit_client.create_kit_with_raw_payload(
            payload=payload,
            auth_token=registered_user_token,
            expected_status=400
        )