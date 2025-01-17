from django.urls import path
from . import views

app_name = "msystem"
urlpatterns = [
    path("", views.index, name="index"),
    path("analytics/", views.analytics, name="analytics"),
    path("clients/", views.clients, name="clients"),
    path("students/", views.students, name="students"),

    path("clients/profile/<int:client_id>", views.client_profile, name="client_profile"),
    path("clients/add", views.add_person, name="add_person"),
    path("clients/update/<int:person_id>", views.update_person, name="update_person"),
    path("clients/set_appointment/<int:client_id>", views.book_client, name="book_client"),
    path("clients/delete/<int:client_id>", views.delete_client, name="delete_client"),

    path("datafiles/add/<int:person_id>", views.add_client_files, name="add_datafiles"),

    path("appointments/", views.appointments, name="appointments"),
    path("appointments/change/<int:ap_id>", views.change_appointment, name="change_appointment"),
    path("appointments/delete/<int:ap_id>", views.delete_appointment, name="delete_appointment"),
    path("appointments/mark/<int:ap_id>", views.mark_appointment, name="mark_appointment"),

    path("employees/", views.employees, name="employees"),
    path("employees/add/<int:person_id>", views.add_employee, name="add_employee"),
    path("employees/update/<int:emp_id>/", views.update_employee, name="update_employee"),

    path("clients/add/request/<int:client_id>", views.add_request, name="add_request"),
    path("clients/request/update/<int:request_id>", views.update_request, name="update_request"),
    path("clients/request/delete/<int:request_id>", views.delete_request, name="delete_request"),

    path("media/analtics/", views.media_dashboard, name="media_dashboard"),
    path("media/topics/", views.media_topics, name="media_topics"),


    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
]