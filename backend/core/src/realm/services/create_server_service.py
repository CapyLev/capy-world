from typing import Any

from src.realm.daos import ServerDAO, CreateServerDTO


class CreateServerService:
    def __init__(self, server_dao: ServerDAO) -> None:
        self._server_dao = server_dao

    def execute(
        self,
        admin_id: int,
        name: str,
        description: str | None,
    ) -> dict[str, Any]:
        create_server_dto = CreateServerDTO(
            admin_id=admin_id,
            name=name,
            description=description,
        )
        result = self._server_dao.create_user_server(data=create_server_dto)
        return result
