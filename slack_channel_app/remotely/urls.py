from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views 

urlpatterns = [
    path("", views.index, name="index"), 
    path("ch/<str:channel_name>", views.fetch_channel, name="channel"),
    path("login/", views.login_view, name="login"), 
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.reqister_user, name="register"), 
    path("search/", views.search, name="search"),
    # url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='login.html'), name="login"), 
    # url(r'^accounts/logout/$', auth_views.LogoutView.as_view(template_name='login.html'), name="logout"),
]