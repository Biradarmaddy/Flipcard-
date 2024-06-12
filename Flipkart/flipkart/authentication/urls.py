from django.urls import path
from . import views


urlpatterns = [
    path("user/signup",views.user_signup,name="signup"),
    path("user/login",views.user_login,name="login"),
    path("user/logout",views.user_logout,name="logout")
]