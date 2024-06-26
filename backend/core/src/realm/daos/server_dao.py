from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.realm.models import Server, ServerMember


@dataclass(frozen=True, slots=True)
class CreateServerDTO:
    admin_id: int
    name: str
    description: str | None
    created_at: datetime


@dataclass(frozen=True, slots=True)
class ServerDTO:
    id: int
    admin_id: int
    name: str
    created_at: datetime
    description: str | None = None


@dataclass(frozen=True, slots=True)
class ServerMembersDTO:
    user_id: int
    is_admin: bool
    username: str
    # TODO: image_url


class ServerDAO:
    def create_user_server(
        self,
        admin_id: int,
        name: str,
        description: str | None = None,
    ) -> CreateServerDTO:
        server = Server.objects.create(
            admin_id=admin_id,
            name=name,
            description=description,
        )
        ServerMember.objects.create(
            server=server,
            user_id=admin_id,
        )

        return CreateServerDTO(
            admin_id=server.admin_id,
            name=server.name,
            description=server.description,
            created_at=server.created_at,
        )

    def check_if_user_already_joined(
        self,
        server_id: int,
        user_id: int,
    ) -> bool:
        return ServerMember.objects.filter(
            server_id=server_id, user_id=user_id
        ).exists()

    def connect_user_to_server(
            self,
            server_id: int,
            user_id: int,
    ) -> None:
        ServerMember.objects.create(
            server_id=server_id,
            user_id=user_id,
        )

    def get_user_servers(self, user_id: int) -> list[ServerDTO]:
        return [
            ServerDTO(
                id=server_member.server_id,
                admin_id=server_member.server.admin_id,
                description=server_member.server.description,
                name=server_member.server.name,
                created_at=server_member.server.created_at,
            )
            for server_member in ServerMember.objects.select_related("server").filter(
                user_id=user_id
            )
        ]

    def get_server_members(self, server_id: int) -> list[ServerMembersDTO]:
        return [
            ServerMembersDTO(
                user_id=server_member.user_id,
                username=server_member.user.username,
                is_admin=True if server_member.server.admin_id == server_member.user_id else False,
            )
            for server_member in ServerMember.objects.select_related(
                "server",
                "user",
            ).filter(
                server_id=server_id,
            )
        ]

    def get_server_by_id(self, server_id: int) -> ServerDTO:
        server = Server.objects.get(id=server_id)
        return ServerDTO(
            id=server.id,
            admin_id=server.admin_id,
            name=server.name,
            created_at=server.created_at,
            description=server.description,
        )
