import pytest

# Intento de importación global para repos
try:
    from src.repos.user import UserRepository
    REPOS_AVAILABLE = True
except ModuleNotFoundError as e:
    REPOS_AVAILABLE = False
    FAIL_REASON = f"Falta módulo o paquete en repos: {e.name}"
except ImportError as e:
    REPOS_AVAILABLE = False
    FAIL_REASON = f"Error de importación en repos: {str(e)}"


def test_repos_user_exists():
    if not REPOS_AVAILABLE:
        pytest.fail(FAIL_REASON, pytrace=False)
    # Si el import fue exitoso, verificamos que la clase UserRepository exista
    assert UserRepository is not None, "La clase UserRepository debería existir en src/repos/user.py"


@pytest.mark.skipif(not REPOS_AVAILABLE, reason=FAIL_REASON)
def test_repository_add_user_increments_id():
    repo = UserRepository()
    new_user = repo.add_user("Charlie")
    assert new_user.id > 0, "El id del nuevo usuario debería ser mayor que 0"
    assert new_user.name == "Charlie", "El nombre del nuevo usuario debería ser 'Charlie'"