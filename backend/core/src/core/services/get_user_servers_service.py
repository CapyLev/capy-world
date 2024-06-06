from src.realm.daos import ServerDAO, ServerDTO


class GetUserServersService:
    def __init__(
        self,
        server_dao: ServerDAO,
    ) -> None:
        self._server_dao = server_dao

    def execute(
        self,
        user_id: int,
    ) -> list[ServerDTO]:
        return self._server_dao.get_user_servers(user_id)
