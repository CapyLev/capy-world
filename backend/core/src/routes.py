from django.urls import include, path

routes = [
    path("profile/", include("src.profile.urls"), name="profile"),
    path("realm/", include("src.realm.urls"), name="realm"),
]
