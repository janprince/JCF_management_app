from django.urls import path
from . import views

app_name = "msystem"
urlpatterns = [
    path("", views.index, name="index"),
    path("clients/add", views.add_person, name="add_person"),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
]