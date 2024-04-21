from sanic import Blueprint
from .views import PingView, TestView

route = Blueprint('core', url_prefix='/core')

route.add_route(PingView.as_view(), '/ping')
route.add_route(TestView.as_view(), '/test')
