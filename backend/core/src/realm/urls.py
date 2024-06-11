from django.urls import path

from .views import HomePageTemplateView, ChatPageTemplateView

urlpatterns = [
    path("", HomePageTemplateView.as_view(), name="home_page"),
    path("<int:server_id>/", ChatPageTemplateView.as_view(), name="chat_page"),
]
