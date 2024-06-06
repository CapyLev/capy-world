from django.urls import path

from .views import HomePageTemplateView, RealmPageTemplateView

urlpatterns = [
    path("", HomePageTemplateView.as_view(), name="home_page"),
    path("<int:server_id>/", RealmPageTemplateView.as_view(), name="realm_page"),
]
