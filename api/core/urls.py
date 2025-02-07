from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import RegisterView, CustomTokenRefreshView, TokenLogoutView, UserView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="refresh"),
    path("logout/", TokenLogoutView.as_view(), name="logout"),
    path("me/", UserView.as_view(), name="me")
]