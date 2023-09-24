from django.contrib import admin
from .models import *


class PersonAdmin(admin.ModelAdmin):
    list_display = ['id', "full_name", "gender", "phone", "country", "is_client", "is_student"]
    list_filter = ('is_student',)
    search_fields = ['full_name']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'role']


class RepAdmin(admin.ModelAdmin):
    list_display = ['id', 'person', 'country']


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'person', 'date', 'mode', "done"]
    actions = ['mark_done']

    def mark_done(self, request, queryset):
        queryset.update(done=True)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["id", 'person', 'role', 'salary']


class RequestAdmin(admin.ModelAdmin):
    list_display = ["id", 'person']


class DataFileAdmin(admin.ModelAdmin):
    list_display = ["id", 'person', 'file']


# Register your models here.
admin.site.register(Person, PersonAdmin)
admin.site.register(Rep, RepAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(DataFile, DataFileAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Profile, ProfileAdmin)
