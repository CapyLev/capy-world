from django.urls import path

from .views import LandingPageTemplateView

urlpatterns = [
    path("", LandingPageTemplateView.as_view(), name="landing_page"),
]
