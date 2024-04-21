from sanic import Request
from sanic.response import JSONResponse
from sanic.views import HTTPMethodView

from src.modules.realm.repository import MessageRepository
from src.modules.realm.services import SendWelcomeMsgService


class SendWelcomeMsgView(HTTPMethodView):
    async def post(self, request: Request) -> JSONResponse:
        data = request.json

        service = SendWelcomeMsgService(
            message_repository=MessageRepository(),
        )
        service.execute(server_id=data["server_id"], username=data["username"])
        return JSONResponse(status=200)
