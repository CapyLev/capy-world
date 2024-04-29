from django.urls import path

from .views import CreateServerView, JoinToServerView

urlpatterns = [
    path("create/", CreateServerView.as_view(), name="create"),
    path("join/", JoinToServerView.as_view(), name="join"),
]
