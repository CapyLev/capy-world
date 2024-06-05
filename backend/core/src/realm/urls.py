from django.urls import path

from .views import HomePageTemplateView

urlpatterns = [
    path('', HomePageTemplateView.as_view(), name='home_page'),
]
