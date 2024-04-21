from django.urls import path

from .view import CreateServerView

urlpatterns = [
    path("create/", CreateServerView.as_view(), name="create"),
]
