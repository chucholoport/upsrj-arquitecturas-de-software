import pytest

# Intento de importación global para models
try:
    from src.models.user import User
    MODELS_AVAILABLE = True
except ModuleNotFoundError as e:
    MODELS_AVAILABLE = False
    FAIL_REASON = f"Falta módulo o paquete en models: {e.name}"
except ImportError as e:
    MODELS_AVAILABLE = False
    FAIL_REASON = f"Error de importación en models: {str(e)}"


def test_models_user_exists():
    if not MODELS_AVAILABLE:
        pytest.fail(FAIL_REASON, pytrace=False)
    # Si el import fue exitoso, verificamos que la clase User exista
    assert User is not None, "La clase User debería existir en src/models/user.py"


@pytest.mark.skipif(not MODELS_AVAILABLE, reason=FAIL_REASON)
def test_user_to_dict_casts_types():
    user = User(id="10", name="Carlos")
    data = user.to_dict()
    assert data == {"id": 10, "name": "Carlos"}, "User.to_dict() debería castear id a entero"