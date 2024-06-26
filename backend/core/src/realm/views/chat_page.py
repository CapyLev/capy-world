from typing import Any

from src.core.views import RealmTemplateView
from ..daos import ServerDAO
from ..services import GetServerDataService


class ChatPageTemplateView(RealmTemplateView):
    template_name = "realm/chat_page.html"

    def get_context_data(
        self,
        server_id: int,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context_service = GetServerDataService(
            server_dao=ServerDAO(),
        )
        data = context_service.execute(server_id)

        context['server_members'] = data.server_members
        context['server_name'] = data.server_name
        context['server_id'] = data.server_id
        return context
