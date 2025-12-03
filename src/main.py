# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Carrera: ISW
# Archivo: main.py
# Descripción: Versión monolítica inicial de la aplicación Flask.
#              Este archivo contiene en un solo lugar la 
#              inicialización de Flask, la configuración básica,
#              la definición de rutas y la lógica de negocio 
#              (listar y crear usuarios). Sirve como punto de 
#              partida antes de modularizar la arquitectura en 
#              capas y separar responsabilidades.
# ============================================================
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

from flask import Flask, jsonify, request


@dataclass
class User:
    """
    Simple DTO for user data with explicit types.
    """
    id: int
    name: str

    def to_dict(self) -> Dict[str, Any]:
        """
        Cast the dataclass to a plain dict with explicit types.
        """
        data = asdict(self)
        # Defensive casting to ensure clean JSON schema
        data["id"] = int(data["id"])
        data["name"] = str(data["name"])
        return data


class UserRepository:
    """
    Repository component that handles user data access.

    Implements the Repository design pattern to abstract data retrieval.
    """

    def __init__(self) -> None:
        """Initialize in-memory storage for users (simulating a database)."""
        self._users: List[User] = [
            User(id=1, name="Alice"),
            User(id=2, name="Bob")
        ]
        self._next_id: int = 3

    def get_users(self) -> List[User]:
        """Return the list of users as DTOs."""
        return self._users

    def add_user(self, name: str) -> User:
        """
        Add a new user to the repository.

        Args:
            name (str): The name of the new user.

        Returns:
            User: The newly created user DTO.
        """
        user = User(id=self._next_id, name=name)
        self._users.append(user)
        self._next_id += 1
        return user


class UserService:
    """
    Service component that contains business logic.

    Uses dependency injection to receive a repository instance.
    """

    def __init__(self, repository: UserRepository) -> None:
        """Initialize the service with a given repository."""
        self.repository = repository

    def list_users(self) -> List[Dict[str, Any]]:
        """
        Retrieve the list of users from the repository, casting to dicts.
        """
        users = self.repository.get_users()
        return [u.to_dict() for u in users]

    def create_user(self, name: str) -> Dict[str, Any]:
        """
        Create a new user, normalizing input and casting to dict.

        - Trims whitespace.
        - Ensures non-empty, reasonable length.
        """
        normalized = str(name).strip()
        if not normalized:
            raise ValueError("Name cannot be empty.")
        if len(normalized) > 100:
            raise ValueError("Name exceeds max length (100).")

        user = self.repository.add_user(normalized)
        return user.to_dict()


app = Flask(__name__)
user_service = UserService(UserRepository())


@app.route("/users", methods=["GET"])
def get_users():
    """
    HTTP endpoint that returns a JSON list of users.

    Always casts to plain dicts with explicit types.
    """
    users = user_service.list_users()
    return jsonify(users), 200


@app.route("/users", methods=["POST"])
def add_user():
    """
    HTTP endpoint to add a new user.

    Expected payload:
    {
        "name": "Charlie"
    }
    """
    data = request.get_json(silent=True) or {}
    name = data.get("name")

    if name is None:
        return jsonify({"error": "Missing 'name' field."}), 400

    try:
        new_user = user_service.create_user(name)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(new_user), 201


if __name__ == "__main__":
    # Entry point: runs the Flask development server in debug mode.
    app.run(host="0.0.0.0", port=5000, debug=True)