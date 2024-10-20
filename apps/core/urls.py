from django.urls import path

from . import views

appname = "core"

urlpatterns = [
    path("ping/", views.ping, name="ping"),
    path("fire-task/", views.fire_task, name="fire_task"),
]
