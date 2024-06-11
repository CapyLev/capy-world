from dataclasses import dataclass

from src.realm.daos import ServerDAO, ServerMembersDTO


@dataclass(frozen=True, slots=True)
class _GetServerDataContexDTO:
    server_members: list[ServerMembersDTO]
    server_name: str


class GetServerDataService:
    def __init__(
        self,
        server_dao: ServerDAO,
    ) -> None:
        self._server_dao = server_dao

    def execute(
        self,
        server_id: int,
    ) -> _GetServerDataContexDTO:
        server_members = self._server_dao.get_server_members(server_id)
        server_name = self._server_dao.get_server_by_id(server_id).name

        return _GetServerDataContexDTO(
            server_members=server_members,
            server_name=server_name,
        )
