from sanic import Blueprint
from .views import send_welcome_msg_view

route = Blueprint("realm", url_prefix="/realm")


route.add_route(send_welcome_msg_view, "/send_welcome_msg")
