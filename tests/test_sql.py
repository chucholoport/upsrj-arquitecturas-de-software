import pytest

try:
    from src.repos.user import UserRepository
    REPOS_AVAILABLE = True
    FAIL_REASON = ""
except ModuleNotFoundError as e:
    REPOS_AVAILABLE = False
    FAIL_REASON = f"Falta módulo o paquete en repos: {e.name}"
except ImportError as e:
    REPOS_AVAILABLE = False
    FAIL_REASON = f"Error de importación en repos: {str(e)}"


def test_repos_uses_sql_connection():
    if not REPOS_AVAILABLE:
        pytest.fail(FAIL_REASON, pytrace=False)

    repo = UserRepository()

    # Verificamos que el repositorio tenga un atributo de conexión SQL
    assert hasattr(repo, "conn"), "UserRepository debería tener un atributo 'conn' para la conexión SQL"
    assert hasattr(repo.conn, "execute"), "La conexión debería permitir ejecutar sentencias SQL"


@pytest.mark.skipif(not REPOS_AVAILABLE, reason=FAIL_REASON or "repos no disponible")
def test_repos_add_and_query_user_sql():
    repo = UserRepository()

    # Insertamos un usuario
    new_user = repo.add_user("Lucía")
    assert new_user.id > 0
    assert new_user.name == "Lucía"

    # Consultamos directamente en SQL para verificar persistencia
    cursor = repo.conn.cursor()
    cursor.execute("SELECT id, name FROM users WHERE id = ?", (new_user.id,))
    row = cursor.fetchone()
    assert row == (new_user.id, "Lucía"), "El usuario debería estar persistido en la tabla SQL"