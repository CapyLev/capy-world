from sanic import Blueprint

from .realm.urls import route as realm_route
from .core.urls import route as core_route


api = Blueprint.group(realm_route, core_route, url_prefix="/api")
