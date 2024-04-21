from dataclasses import dataclass
from typing import Any

from src.realm.models import Server, ServerMember


@dataclass(frozen=True)
class CreateServerDTO:
    admin_id: int
    name: str
    description: str | None
    image: str | None


class ServerDAO:
    def create_user_server(self, data: CreateServerDTO) -> dict[str, Any]:
        server = Server.objects.create(
            admin_id=data.admin_id,
            name=data.name,
            description=data.description,
            image=data.image,
        )
        ServerMember.objects.create(
            server=server,
            user_id=data.admin_id,
        )

        return {
            "admin_id": server.admin_id,
            "name": server.name,
            "description": server.description,
            "image": server.image,
            "created_at": server.created_at,
        }

    def check_if_user_already_joined(
        self,
        server_id: int,
        user_id: int,
    ) -> bool:
        return ServerMember.objects.filter(
            server_id=server_id,
            user_id=user_id
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

