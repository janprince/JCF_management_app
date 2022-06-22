from django.urls import path
from . import views

app_name = "msystem"
urlpatterns = [
    path("", views.index, name="index"),
    path("clients/", views.clients, name="clients"),
    path("students/", views.students, name="students"),
    path("clients/profile/<int:client_id>", views.client_profile, name="client_profile"),
    path("clients/add", views.add_person, name="add_person"),
    path("clients/update/<int:person_id>", views.update_person, name="update_person"),
    path("clients/set_appointment/<int:client_id>", views.book_client, name="book_client"),
    path("appointments/", views.appointments, name="appointments"),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
]