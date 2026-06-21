# 🚀 Urban Grocers API Test Automation Framework

API test automation framework for **Urban Grocers**, implemented in **Python** with **Pytest** and an object-oriented design. This framework verifies user creation and product-kit creation flows with a focused test matrix for the `name` field (9 test scenarios). It demonstrates advanced API automation practices: HTTP session management, reusable fixtures, parametrized tests, and dynamic test-data generation.

---

## 🧠 Technologies and Techniques

| Tecnología / Técnica                | Propósito                                                                                                                |
|-------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| **Python 3.14.5**                   | Primary language                                                                                                         |
| **Pytest 9.0.3**                    | Test framework (parametrization, fixtures, assertions)                                                                  |
| **Requests 2.34.2**                 | HTTP client for exercising the REST API                                                                                 |
| **OOP (inheritance, encapsulation)**| Abstract `BaseClient` with concrete `UserClient` and `KitClient` implementations                                       |
| **Context Managers (`with`)**       | Ensures HTTP sessions are closed automatically                                                                           |
| **Pytest Fixtures**                 | Reusable clients, auth tokens, and test-data setup                                                                      |
| **Environment variables**           | Dynamic configuration (server URL, timeouts, log level)                                                                 |
| **Test data generation**            | `Faker 40.21.0` plus custom logic for producing valid business-oriented data (names, phones, addresses, precise-length kit names) |
| **Logging**                         | Configurable logging (INFO / DEBUG) to inspect request/response payloads                                                |
| **Contract validation**             | Automated checks comparing sent payloads and API responses                                                             |

---

## 📁 Project Structure (clean, maintainable design)

```
urban-grocers-api-tests/
├── config/ # Set environment variables
├── core/ # HTTP Base Client (BaseClient)
├── api_clients/ # Specific clients (UserClient, KitClient)
├── utils/ # (data_generator.py)
├── tests/ # Parametrized tests
├── conftest.py # Global fixtures (base_client, auth token)
├── requirements.txt # Dependencias
├── .env.example # Environment variables template
└── README.md # This file
```

---

## ✅ Test Coverage (9 checkpoints for the `name` field)

| # | Escenario                | Payload `{"name": ...}`       | Código esperado | Resultado                 |
|---|--------------------------|-------------------------------|-----------------|---------------------------|
| 1 | Single character         | `"a"`                         | 201             | ✅ PASS                    |
| 2 | 511 characters          | 511-character string (letters/spaces) | 201       | ✅ PASS                    |
| 3 | Empty string            | `""`                          | 400             | ❌ FAIL (API returns 201)  |
| 4 | 512 characters         | 512-character string (letters/spaces) | 400       | ❌ FAIL (API returns 201)  |
| 5 | Special characters      | `"№%@\","`                | 201             | ✅ PASS                    |
| 6 | Leading/trailing spaces | `" A Aaa "`                   | 201             | ✅ PASS                    |
| 7 | Numbers only           | `"123"`                       | 201             | ✅ PASS                    |
| 8 | Missing `name` param   | `{}`                            | 400             | ❌ FAIL (KeyError in test) |
| 9 | Wrong type (number)    | `123` (not quoted)              | 400             | ❌ FAIL (API returns 201)  |

> **Note:** Failures indicate discrepancies between API documentation and observed behavior. The framework's purpose is to detect and report these inconsistencies so developers and API owners can triage them.

---

## ▶️ Running the tests

The server base URL is generated dynamically by TripleTen and expires after a short time. Do NOT hardcode the URL into project files; pass it as an environment variable when running tests.

Quick run steps:

1. Open a terminal (PowerShell, CMD, or bash) and change directory to the project root:
```bash
cd path/to/project/urban-grocers-automated-api-testing
```
2. (Optional) Activate your virtual environment:
- Windows: .venv\Scripts\activate
- Linux/macOS: source .venv/bin/activate

3. Copy the temporary URL produced by TripleTen when the test server starts.
Example: https://cnt-47557993-38e5-45a3-8932-e46160c6178a.containerhub.tripleten-services.com

4. Run the targeted test file, replacing <your-server> with the real URL:
- PowerShell (Windows)
```powershell
$env:BASE_URL="https://<your-server>.tripleten-services.com"; $env:LOG_LEVEL="INFO"; pytest tests/test_user_kit_creation.py -v
```
- CMD (Windows)
```cmd
set BASE_URL=https://<your-server>.tripleten-services.com && set LOG_LEVEL=INFO && pytest tests/test_user_kit_creation.py -v
```
- Linux / macOS (bash/zsh)
```bash
BASE_URL=https://<your-server>.tripleten-services.com LOG_LEVEL=INFO pytest tests/test_user_kit_creation.py -v
```

Notes:
- `LOG_LEVEL` is optional and defaults to `INFO`. Set it to `DEBUG` to print request/response bodies for troubleshooting.
- To run the full test suite use `pytest tests/`.