import pytest

# Intento de importación global para interfaces
try:
    from src.interfaces.user import IUserRepository, IUserService
    INTERFACES_AVAILABLE = True
except ModuleNotFoundError as e:
    INTERFACES_AVAILABLE = False
    FAIL_REASON_INTERFACES = f"Falta módulo o paquete en interfaces: {e.name}"
except ImportError as e:
    INTERFACES_AVAILABLE = False
    FAIL_REASON_INTERFACES = f"Error de importación en interfaces: {str(e)}"

# Intento de importación global para repositorios
try:
    from src.repos.user import UserRepository
    from src.interfaces.user import IUserRepository
    REPOS_AVAILABLE = True
except ModuleNotFoundError as e:
    REPOS_AVAILABLE = False
    FAIL_REASON_REPOS = f"Falta módulo o paquete en repos/interfaces: {e.name}"
except ImportError as e:
    REPOS_AVAILABLE = False
    FAIL_REASON_REPOS = f"Error de importación en repos/interfaces: {str(e)}"


def test_interfaces_user_exists():
    if not INTERFACES_AVAILABLE:
        pytest.fail(FAIL_REASON_INTERFACES, pytrace=False)
    # Si el import fue exitoso, verificamos que las interfaces existan
    assert IUserRepository is not None, "La interfaz IUserRepository debería existir en src/interfaces/user.py"
    assert IUserService is not None, "La interfaz IUserService debería existir en src/interfaces/user.py"


@pytest.mark.skipif(not REPOS_AVAILABLE, reason=FAIL_REASON_REPOS)
def test_repository_implements_interface():
    repo = UserRepository()
    assert isinstance(repo, IUserRepository), "UserRepository debería implementar la interfaz IUserRepository"