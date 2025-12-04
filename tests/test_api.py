import pytest

# Intento de importación global
try:
    from src.app.main import app
    APP_AVAILABLE = True
except ModuleNotFoundError as e:
    APP_AVAILABLE = False
    FAIL_REASON = f"Falta módulo o paquete en app: {e.name}"
except ImportError as e:
    APP_AVAILABLE = False
    FAIL_REASON = f"Error de importación en app: {str(e)}"


def test_import_app():
    if not APP_AVAILABLE:
        pytest.fail(FAIL_REASON, pytrace=False)


@pytest.mark.skipif(not APP_AVAILABLE, reason=FAIL_REASON)
def test_api_get_users():
    app.testing = True
    client = app.test_client()
    response = client.get("/api/users")
    assert response.status_code == 200, "La ruta /api/users debería devolver 200 OK"
    assert isinstance(response.get_json(), list)


@pytest.mark.skipif(not APP_AVAILABLE, reason=FAIL_REASON)
def test_api_post_users_success():
    app.testing = True
    client = app.test_client()
    response = client.post("/api/users/new", json={"name": "Eva"})
    assert response.status_code == 201, "La ruta /api/users/new debería devolver 201 Created"
    assert response.get_json()["name"] == "Eva"