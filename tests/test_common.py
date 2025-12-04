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


def test_app_main_exists():
    if not APP_AVAILABLE:
        pytest.fail(FAIL_REASON, pytrace=False)
    # Si el import fue exitoso, simplemente verificamos que app exista
    assert app is not None, "El objeto app debería estar definido en src/app/main.py"


@pytest.mark.skipif(not APP_AVAILABLE, reason=FAIL_REASON)
def test_app_has_testing_mode():
    app.testing = True
    assert app.testing is True, "El objeto app debería permitir activar el modo testing"