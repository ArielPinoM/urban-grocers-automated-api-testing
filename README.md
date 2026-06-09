# 🚀 Urban Grocers API Test Automation Framework

Framework de automatización de pruebas para la API de **Urban Grocers**, diseñado con **Python**, **Pytest** y un estricto enfoque de **Programación Orientada a Objetos (POO)**.  
Valida la creación de usuarios y la creación de kits de productos, con especial énfasis en el campo `name` (9 casos de prueba). Ideal para demostrar habilidades avanzadas en automatización de APIs, manejo de sesiones HTTP, fixtures reutilizables y generación dinámica de datos.

---

## 🧠 Tecnologías y técnicas utilizadas

| Tecnología / Técnica                | Propósito                                                                                                         |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| **Python 3.14.5**                   | Lenguaje principal                                                                                                |
| **Pytest 9.0.3**                    | Framework de pruebas (parametrización, fixtures, aserciones)                                                      |
| **Requests 2.34.2**                       | Cliente HTTP para consumir la API REST                                                                            |
| **POO (Herencia, encapsulamiento)** | `BaseClient` abstracto + `UserClient` / `KitClient` específicos                                                   |
| **Context Managers (`with`)**       | Cierre automático de sesiones HTTP                                                                                |
| **Fixtures de Pytest**              | Reutilización de clientes, token de autenticación, datos de prueba                                                |
| **Variables de entorno**            | Configuración dinámica (URL de servidor, timeouts, nivel de log)                                                  |
| **Generación de datos**             | `Faker 40.21.0` + lógica personalizada para datos válidos (nombres, teléfonos, direcciones, kits con longitudes exactas) |
| **Manejo de logs**                  | Logging configurable (INFO / DEBUG) para seguimiento de peticiones                                                |
| **Validación de contratos**         | Comparación automática entre payload enviado y respuesta recibida                                                 |

---

## 📁 Estructura del proyecto (diseño limpio y mantenible)

```
urban-grocers-api-tests/
├── config/ # Configuración desde variables de entorno
├── core/ # Cliente base HTTP (BaseClient) y excepciones
├── api_clients/ # Clientes específicos (UserClient, KitClient)
├── models/ # Modelos de datos (placeholders para futuro tipado)
├── utils/ # Generadores de datos (data_generator.py)
├── tests/ # Casos de prueba parametrizados
├── conftest.py # Fixtures globales (base_client, auth token)
├── requirements.txt # Dependencias
├── .env.example # Plantilla de variables de entorno
└── README.md # Este archivo
```

---

## ✅ Cobertura de pruebas (9 checkpoints en el campo `name`)

| # | Escenario | Payload `{"name": ...}` | Código esperado | Resultado |
|---|-----------|------------------------|----------------|-----------|
| 1 | 1 carácter | `"a"` | 201 | ✅ PASS |
| 2 | 511 caracteres | string de 511 letras/espacios | 201 | ✅ PASS |
| 3 | 0 caracteres | `""` | 400 | ❌ FAIL (API devuelve 201) |
| 4 | 512 caracteres | string de 512 letras/espacios | 400 | ❌ FAIL (API devuelve 201) |
| 5 | Caracteres especiales | `"№%@\","` | 201 | ✅ PASS |
| 6 | Espacios | `" A Aaa "` | 201 | ✅ PASS |
| 7 | Solo números | `"123"` | 201 | ✅ PASS |
| 8 | Parámetro `name` ausente | `{}` | 400 | ❌ FAIL (KeyError en test) |
| 9 | Tipo incorrecto (número) | `123` (sin comillas) | 400 | ❌ FAIL (API devuelve 201) |

> **Nota:** Los fallos detectados demuestran discrepancias entre la documentación y el comportamiento real de la API. El framework cumple su función: **alertar sobre inconsistencias**.

---

## ▶️ Ejecución de las pruebas

La URL base del servidor se genera automáticamente al iniciar el servidor en el portal de **TripleTen** y **caduca después de un tiempo**. Por lo tanto, **no debe guardarse** en archivos de configuración fijos, sino pasarse como variable de entorno cada vez que ejecutes las pruebas.

Sigue estos pasos:

1. **Abre una terminal** (PowerShell, CMD, o bash) y navega hasta la raíz del proyecto:
   ```bash
   cd ruta/del/proyecto/urban-grocers-automated-api-testing
   
2. **Activa el entorno virtual** (opcional pero recomendado):
- Windows: .venv\Scripts\activate
- Linux/Mac: source .venv/bin/activate

3. **Copia la URL** que te proporciona TripleTen al iniciar el servidor.
- Ejemplo: https://cnt-47557993-38e5-45a3-8932-e46160c6178a.containerhub.tripleten-services.com
4. **Ejecuta el comando correspondiente a tu sistema operativo**, reemplazando <tu-servidor> por la URL real:
- PowerShell (Windows)
```text
$env:BASE_URL="https://<tu-servidor>.tripleten-services.com"; $env:LOG_LEVEL="INFO"; pytest tests/test_user_kit_creation.py -v
```
- CMD (Windows)
```text
set BASE_URL=https://<tu-servidor>.tripleten-services.com && set LOG_LEVEL=INFO && pytest tests/test_user_kit_creation.py -v
```
- Linux / macOS (bash/zsh)
```text
BASE_URL=https://<tu-servidor>.tripleten-services.com LOG_LEVEL=INFO pytest tests/test_user_kit_creation.py -v
```

> Nota
> - La variable LOG_LEVEL es opcional. Por defecto se usa INFO. Si cambias su valor a DEBUG, verás en la consola los cuerpos de las peticiones y respuestas, útil para depurar fallos.
> - También puedes ejecutar todas las pruebas del proyecto usando pytest tests/ en lugar de apuntar a un archivo específico.