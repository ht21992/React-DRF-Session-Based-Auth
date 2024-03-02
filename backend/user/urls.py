from django.urls import path
from . import views

urlpatterns = [
    path("is_authenticated/", views.CheckAuthenticatedView.as_view(),
         name="check_authentication"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("csrf_cookie/", views.GetCSRFToken.as_view(), name="csrf"),
    path("", views.getRoutes, name="get_routes"),
]
