from django.urls import path

from .views import CreateServerView

urlpatterns = [
    path("create/", CreateServerView.as_view(), name="create"),
]
