from sanic import Blueprint
from .views import SendWelcomeMsgView


route = Blueprint('realm', url_prefix='/realm')

route.add_route(SendWelcomeMsgView.as_view(), '/send_welcome_msg')
