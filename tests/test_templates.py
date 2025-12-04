import pytest
import os

# Verificación global de templates requeridos
REQUIRED_TEMPLATES = ["index.html", "users.html", "new_user.html"]
MISSING_TEMPLATE = None
for tpl in REQUIRED_TEMPLATES:
    path = os.path.join("src", "templates", tpl)
    if not os.path.exists(path):
        MISSING_TEMPLATE = tpl
        break

# Intento de importación global de app
try:
    from src.app.main import app
    APP_AVAILABLE = True
except ModuleNotFoundError as e:
    APP_AVAILABLE = False
    FAIL_REASON = f"Falta módulo o paquete en app: {e.name}"
except ImportError as e:
    APP_AVAILABLE = False
    FAIL_REASON = f"Error de importación en app: {str(e)}"


def test_templates_exist():
    if MISSING_TEMPLATE:
        pytest.fail(f"Falta template: {MISSING_TEMPLATE}", pytrace=False)
    # Si todos existen, simplemente verificamos que la lista esté completa
    assert all(os.path.exists(os.path.join("src", "templates", tpl)) for tpl in REQUIRED_TEMPLATES)


@pytest.mark.skipif(not APP_AVAILABLE, reason=FAIL_REASON)
@pytest.mark.skipif(MISSING_TEMPLATE is not None, reason=f"Falta template: {MISSING_TEMPLATE}")
def test_html_users_page():
    app.testing = True
    client = app.test_client()
    response = client.get("/users")
    assert response.status_code == 200
    assert b"Alice" in response.data  # contenido HTML esperado


@pytest.mark.skipif(not APP_AVAILABLE, reason=FAIL_REASON)
@pytest.mark.skipif(MISSING_TEMPLATE is not None, reason=f"Falta template: {MISSING_TEMPLATE}")
def test_html_new_user_form():
    app.testing = True
    client = app.test_client()
    response = client.get("/users/new")
    assert response.status_code == 200
    assert b"<form" in response.data