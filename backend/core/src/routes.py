from django.urls import include, path

routes = [
    path("account/", include("src.account.urls"), name="account"),
    path("realm/", include("src.realm.urls"), name="realm"),
]
