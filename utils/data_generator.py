"""
Dynamic test data generator for the Urban Grocers API.

Uses Faker to produce realistic, business-rule-compliant test data.
"""


from faker import Faker
import random
import string


# Configure locale to produce Latin-alphabet names (avoids non-latin characters)
fake = Faker('es_ES')  # Spanish locale to generate Latin-based names


def generate_valid_first_name(min_length: int = 2, max_length: int = 15) -> str:
    """
    Generate a valid first name (Latin letters only, length between 2 and 15).

    Args:
        min_length: Minimum length (default 2)
        max_length: Maximum length (default 15)

    Returns:
        A name that complies with validation rules.
    """
    # Faker typically produces valid names, but we enforce length and allowed chars.
    # Use ASCII letters to guarantee Latin-only characters.
    allowed_chars = string.ascii_letters
    # Generamos una longitud aleatoria dentro del rango
    length = random.randint(min_length, max_length)
    name = ''.join(random.choice(allowed_chars) for _ in range(length))
    # Capitalizamos la primera letra
    return name.capitalize()

def generate_valid_phone() -> str:
    """
    Generate a valid phone number in international format (leading '+').

    Returns:
        Example: +11234567890
    """
    # Generate 10-12 digits after the country code
    digits_count = random.randint(10, 12)
    digits = ''.join(str(random.randint(0, 9)) for _ in range(digits_count))
    return f'+1{digits}'

def generate_valid_address(min_length: int = 5, max_length: int = 50) -> str:
    """
    Generate a valid address: Latin characters, spaces, punctuation, length 5-50.

    Returns:
        A random valid address string.
    """
    address = fake.street_address()
    # Asegurar longitud de rango
    if len(address) < min_length:
        address = address + ' ' + fake.city()[:min_length - len(address)]
    elif len(address) > max_length:
        address = address[:max_length]
    return address

def generate_user_payload(include_optional: bool = False) -> dict:
    """
    Generate a full payload for user creation.

    Args:
        include_optional: If True, include optional `email` and `comment` fields.

    Returns:
        A dict containing required (and optional) fields.
    """
    payload = {
        "firstName": generate_valid_first_name(),
        "phone": generate_valid_phone(),
        "address": generate_valid_address(),
    }
    if include_optional:
        payload["email"] = fake.email()
        payload["comment"] = fake.sentence()
    return payload

def generate_kit_name(length: int) -> str:
    """
    Generate a kit name with a specific length.

    Args:
        length: Desired string length

    Returns:
        String of exactly `length` characters (Latin letters + spaces).
    """
    if length == 0:
        return ''
    # Usar letras ascii + espacios para simular nombre válido (evita caracteres no latinos)
    chars = string.ascii_letters + ' '
    # Asegurar que el nombre no empiece o termine con espacio (opcional, pero evita problemas)
    name = ''.join(random.choice(chars) for _ in range(length))
    return name

def generate_kit_name_with_special_chars(length: int) -> str:
    """
    Generate a kit name containing special characters (e.g. "№%@,").

    Args:
        length: Desired length

    Returns:
        String that may include special characters.
    """
    specials = "№%@\","
    # Mezcla caracteres especiales y algunos normales
    chars = specials + string.ascii_letters
    return ''.join(random.choice(chars) for _ in range(length))

def generate_kit_name_with_spaces(length: int = 6) -> str:
    """
    Generate a kit name that includes leading, internal, and trailing spaces.

    Args:
        length: Total length including spaces.

    Returns:
        Example string like " A Aaa " (with spaces around).
    """
    if length < 3:
        return " A "
        # Crear patrón: espacio + letras + espacio + letras + espacio
    middle = generate_kit_name(length - 3)
    return f" {middle[:length - 3]} "