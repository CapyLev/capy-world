from sanic import Blueprint
from .views import send_welcome_msg_view, message_handler_view

route = Blueprint("realm", url_prefix="/realm")


route.add_route(
    handler=send_welcome_msg_view,
    uri="/send_welcome_msg",
    name="send_welcome_msg",
)
route.add_websocket_route(
    handler=message_handler_view,
    uri="/ws/message_handler/<server_id:int>/<user_id:int>",
    name="message_handler",
)
