from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path, include
from rest_framework import routers
from rest_framework.permissions import IsAuthenticated

from .yasg import generate_api_description, SurveySchemaGenerator
from .views import NetworkViewSet, UserViewSet, LikeViewSet

router = routers.SimpleRouter()
router.register("post", NetworkViewSet)
router.register("users", UserViewSet)
router.register("analytics", LikeViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
urlpatterns += router.urls

schema_view = get_schema_view(
    openapi.Info(
        title="Social Network API",
        default_version="v1",
        description=generate_api_description(),
    ),
    public=False,
    permission_classes=(IsAuthenticated,),
    generator_class=SurveySchemaGenerator,
    patterns=urlpatterns,
)

urlpatterns += [
    path(
        "swagger/<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="swagger-yaml",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
