from django.urls import path

from . import views 

urlpatterns = [
    path("", views.index, name="index"), 
    path("<str:channel_name>", views.fetch_channel, name="channel")
]