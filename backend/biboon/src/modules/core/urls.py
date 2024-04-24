from sanic import Blueprint
from .views import ping_view, test_mongo_view, test_rabbit_view

route = Blueprint("core", url_prefix="/core")


route.add_route(ping_view, "/ping")
route.add_route(test_mongo_view, "/test_mongo")
route.add_route(test_rabbit_view, "/test_rabbit")
