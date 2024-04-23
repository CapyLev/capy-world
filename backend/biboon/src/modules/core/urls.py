from sanic import Blueprint
from .views import ping_view, test_view

route = Blueprint("core", url_prefix="/core")


route.add_route(ping_view, "/ping")
route.add_route(test_view, "/test")
