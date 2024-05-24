from django.urls import path

from .views import CreateServerView, JoinToServerView

urlpatterns = [
    path("create/", CreateServerView, name="create"),
    path("join/", JoinToServerView, name="join"),
]
