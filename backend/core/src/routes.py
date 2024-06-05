from django.urls import include, path

routes = [
    path("profile/", include("src.profile.urls"), name="profile"),
    path("realm/", include("src.realm.urls"), name="realm"),
    path("account/", include("src.account.urls"), name="account"),
    path("", include("src.landing.urls"), name="landing"),
]
