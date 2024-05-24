from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Capy-World Core",
        default_version="v0.0.1",
    ),
    public=True,
    urlconf="config.urls",
)
