from django.urls import path

from . import views

app_name = "lichca"

urlpatterns = [
    path("", views.home, name="home"),
]
