from django.views.generic.base import ContextMixin

from src.core.services import GetUserServersService
from src.realm.daos import ServerDAO


class UserServersMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id

        service = GetUserServersService(server_dao=ServerDAO())
        user_servers = service.execute(user_id)

        context["user_servers"] = user_servers
        return context
