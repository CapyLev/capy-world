from django.urls import path

from .views import CreateServerView, JoinToServerView, GetUserServersView

urlpatterns = [
    path("create/", CreateServerView.as_view(), name="create"),
    path("join/", JoinToServerView.as_view(), name="join"),
    path("", GetUserServersView.as_view(), name="get"),
]
