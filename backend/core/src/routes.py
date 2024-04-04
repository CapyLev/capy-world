from django.urls import include, path

routes = [
    path("account/", include("src.account.urls"), name="account"),
]
