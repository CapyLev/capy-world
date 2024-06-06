from typing import Any

from src.realm.daos import ServerDAO


class GetUserServersService:
    def __init__(
        self,
        server_dao: ServerDAO,
    ) -> None:
        self._server_dao = server_dao

    def execute(
        self,
        user_id: int,
    ) -> dict[str, Any]:
        user_servers_dto = self._server_dao.get_user_servers(user_id)

        return {
            "servers": [
                {
                    "id": user_server_dto.id,
                    "name": user_server_dto.name,
                    "description": user_server_dto.description,
                    "admin_id": user_server_dto.admin_id,
                    "created_at": user_server_dto.created_at,
                }
                for user_server_dto in user_servers_dto.servers
            ]
        }
