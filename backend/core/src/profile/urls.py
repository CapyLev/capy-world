from django.urls import path, include

from .views import GetUserDetailsView


urlpatterns = [
    path('account', include('django.contrib.auth.urls')),
    path('account/user/<int:pk>', GetUserDetailsView.as_view(), name='account-user'),
]
