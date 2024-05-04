from typing import Any

from src.realm.daos import ServerDAO


class CreateServerService:
    def __init__(self, server_dao: ServerDAO) -> None:
        self._server_dao = server_dao

    def execute(
        self,
        admin_id: int,
        name: str,
        description: str | None,
    ) -> dict[str, Any]:
        result = self._server_dao.create_user_server(
            admin_id=admin_id,
            name=name,
            description=description,
        )

        return {
            "admin_id": result.admin_id,
            "name": result.name,
            "description": result.description,
            "created_at": result.created_at,
        }
