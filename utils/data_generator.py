"""
Generador de datos de prueba dinámicos para Urban Grocers API.

Utiliza Faker para crear datos realistas pero válidos según las reglas de negocio.
"""


from faker import Faker
import random
import string


# Configurar locale para nombres en alfabeto latino (evita caracteres no latinos)
fake = Faker('es_ES') # Usa español pero mantiene letras latinas


def generate_valid_first_name(min_length: int = 2, max_length: int = 15) -> str:
    """
    Genera un nombre válido (solo letras latinas, longitud entre 2 y 15).

    Args:
        min_length: Longitud minima (default 2)
        max_length: Longitud maxima (default 15)

    Returns:
        Nombre que cumple las reglas de validación
    """
    # Faker genera nombres reales que normalmente cumplen, pero forzamos longitud
    name = fake.first_name()
    if len(name) < min_length:
        name = name + fake.random_letter() * (min_length - len(name))
    elif len(name) > max_length:
        name = name[:max_length]
    return name

def generate_valid_phone() -> str:
    """
    Genera un número de teléfono valido: solo números y signo +, formato internacional.

    Returns:
        Ejemplo: +34612345678
    """
    # Genera número de 10-12 dígitos después del +
    digits = ''.join(str(random.randint(0, 9)) for _ in range(random.randint(10, 12)))
    return f'+{digits}'

def generate_valid_address(min_length: int = 5, max_length: int = 50) -> str:
    """
    Genera una dirección válida: letras latinas, espacios, puntuación, longitud 5-50.

    Returns:
        Dirección aleatoria válida
    """
    address = fake.stree_address()
    # Asegurar longitud de rango
    if len(address) < min_length:
        address = address + ' ' + fake.city()[:min_length - len(address)]
    elif len(address) > max_length:
        address = address[:max_length]
    return address

def generate_user_payload(include_optional: bool = False) -> dict:
    """
    Genera un payload completo para creación de usuario.

    Args:
        include_optional: Si True, incluye email y comment (opcionales)

    Returns:
        Diccionario con campos requeridos (y opcionales según flag)
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
    Genera un nombre de kit con una longitud específica.

    Args:
        length: Longitud deseada del string

    Returns:
        String de exactamente 'length' caracteres (letras latinas + espacios)
    """
    if length == 0:
        return ''
    # Usar letras ascii + espacios para simular nombre válido (evita caracteres no latinos)
    chars = string.ascii_letters + ' '
    # Asegurar que el nombre no empiece o termine con espacio (opcional, pero evita problemas)
    name = ''.join(random.choice(chars) for _ in range(length))
    return name

def generate_kit_name_with_special_chars(length: int = 5) -> str:
    """
    Genera un nombre de kit con caracteres especiales (ej.: "№%@",)

    Args:
        length: Longitud deseada

    Returns:
        String con caracteres especiales
    """
    specials = "№%@\","
    # Mezcla caracteres especiales y algunos normales
    chars = specials + string.ascii_letters
    return ''.join(random.choice(chars) for _ in range(length))

def generate_kit_name_with_spaces(length: int = 6) -> str:
    """
    Genera un nombre de kit con espacios al inicio, interior y final.

    Args:
        length: Longitud total incluyendo espacios.

    Returns:
        String como " A Aaa " (espacios alrededor).
    """
    if length < 3:
        return " A "
        # Crear patrón: espacio + letras + espacio + letras + espacio
    middle = generate_kit_name(length - 3)
    return f" {middle[:length - 3]} "