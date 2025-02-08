from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="RESTful API for Authentication",
        default_version="v1",
        description="""REST API for a user authentication and authorization system uses Django and Django REST Framework. The system supports user registration, authentication, token refresh, logout, and allows users to retrieve and update their personal information. Authentication utilizes Access and Refresh tokens.
        Refresh Token – A UUID stored in the database, issued for 30 days by default.
        Access Token – A JSON Web Token with a default lifespan of 30 seconds.
        Clients may request an Access Token refresh at any time, for instance, upon Access Token expiry by providing a valid Refresh Token. In this case, the service returns a new valid pair of Access and Refresh Tokens, resetting their lifespans.
        """
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include('core.urls')),
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]