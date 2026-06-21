"""
Automated tests for product-kit creation in Urban Grocers.

Validate the `name` field against the defined checklist.
"""

import pytest
from utils.data_generator import generate_kit_name, generate_kit_name_with_special_chars, generate_kit_name_with_spaces


class TestKitCreation:
    """Test class grouping all kit-creation related cases."""
    @pytest.mark.parametrize(
        "kit_name, expected_status, should_check_name",
        [
            # Test 1: single character (allowed, should create kit)
            ("a", 201, True),
            # Test 2: 511 characters (allowed, should create kit)
            (generate_kit_name(511), 201, True),
            # Test 3: empty string (not allowed, expect 400)
            ("", 400, False),
            # Test 4: 512 characters (not allowed, expect 400)
            (generate_kit_name(512), 400, False),
            # Test 5: special characters (allowed, should create kit)
            (generate_kit_name_with_special_chars(5), 201, True),
            # Test 6: spaces (allowed, should create kit)
            (generate_kit_name_with_spaces(6), 201, True),
            # Test 7: numbers only (allowed, should create kit)
            ("123", 201, True),
            # Test 8: missing 'name' parameter (empty payload, expect 400)
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
        Parametrized test that validates the `name` field when creating kits.
        """
        # Construir payload según sea el caso
        if kit_name is None:
            payload = {}
        else:
            payload = {"name": kit_name}

        # Send request using the method that accepts raw payloads
        response = kit_client.create_kit_with_raw_payload(
            payload=payload,
            auth_token=registered_user_token,
            expected_status=expected_status
        )

        # Verify the returned name matches when creation succeeds and a match is expected
        if expected_status == 201 and should_check_name and kit_name is not None:
            assert response["name"] == kit_name, \
                f"The response name ({response['name']}) does not match the sent value ({kit_name})"

    def test_kit_name_with_integer_type(self, kit_client, registered_user_token):
        """
        Test 9: pass a number instead of a string as the `name` value.

        The API should respond with a 400 error.
        """
        payload = {"name": 123}
        kit_client.create_kit_with_raw_payload(
            payload=payload,
            auth_token=registered_user_token,
            expected_status=400
        )