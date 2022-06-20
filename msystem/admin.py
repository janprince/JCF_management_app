from django.contrib import admin
from .models import *


class PersonAdmin(admin.ModelAdmin):
    list_display = ['id', "full_name", "gender", "phone", "country", "is_client", "is_student"]


class RepAdmin(admin.ModelAdmin):
    list_display = ['id', 'person', 'country']


class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'person', 'date', 'modes']


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["id", 'person', 'role', 'salary']


class DataFileAdmin(admin.ModelAdmin):
    list_display = ["id", 'person', 'file']


# Register your models here.
admin.site.register(Person, PersonAdmin)
admin.site.register(Rep, RepAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(DataFile, DataFileAdmin)