import pytest

# Intento de importación global para services y repos
try:
    from src.services.user import UserService
    from src.repos.user import UserRepository
    SERVICES_AVAILABLE = True
except ModuleNotFoundError as e:
    SERVICES_AVAILABLE = False
    FAIL_REASON = f"Falta módulo o paquete en services/repos: {e.name}"
except ImportError as e:
    SERVICES_AVAILABLE = False
    FAIL_REASON = f"Error de importación en services/repos: {str(e)}"


def test_services_user_exists():
    if not SERVICES_AVAILABLE:
        pytest.fail(FAIL_REASON, pytrace=False)
    # Si el import fue exitoso, verificamos que la clase UserService exista
    assert UserService is not None, "La clase UserService debería existir en src/services/user.py"


@pytest.mark.skipif(not SERVICES_AVAILABLE, reason=FAIL_REASON)
def test_service_create_user_validations():
    service = UserService(UserRepository())
    user = service.create_user("   Diana   ")
    assert user["name"] == "Diana", "UserService.create_user debería normalizar el nombre"

    with pytest.raises(ValueError):
        service.create_user("   ")