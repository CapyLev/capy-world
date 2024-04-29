from src.realm.daos import ServerDAO, BiboonDAO


class JoinToServerService:
    def __init__(
        self,
        server_dao: ServerDAO,
        biboon_dao: BiboonDAO,
    ) -> None:
        self._server_dao = server_dao
        self._biboon_dao = biboon_dao

    class JoinToServerServiceError(Exception):
        pass

    class UserAlreadyExistsError(JoinToServerServiceError):
        pass

    def execute(self, server_id: int, user_id: int) -> None:
        if not self._server_dao.check_if_user_already_joined(server_id, user_id):
            raise self.UserAlreadyExistsError

        self._server_dao.connect_user_to_server(server_id, user_id)
        self._biboon_dao.send_welcome_message(
            server_id=server_id,
            user_id=user_id,
        )
