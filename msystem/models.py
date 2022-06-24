from django.db import models
from datetime import date


# Person
class Person(models.Model):
    GENDERS = [("Male", "Male"), ("Female", "Female")]
    date_added = models.DateField(auto_now_add=True)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDERS, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=255)
    profession = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    religion = models.CharField(max_length=255, default="N/A")
    residence = models.CharField(max_length=255, blank=True)
    hometown = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, default="Ghana")
    f_name = models.CharField(max_length=255, blank=True)
    m_name = models.CharField(max_length=255, blank=True)
    request_info = models.TextField(blank=True)
    remark = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    referral = models.CharField(max_length=255, blank=True)
    is_client = models.BooleanField(blank=True, default=True)
    is_student = models.BooleanField(default=False)

    class Meta:
        unique_together = ["full_name", "phone"]

    def __str__(self):
        return f"{self.full_name}"


# File Attachment
class DataFile(models.Model):
    person = models.ForeignKey(Person, related_name="datafiles", on_delete=models.RESTRICT)
    file = models.FileField(upload_to="data-files")

    def extension(self):
        import os
        name, extension = os.path.splitext(self.file.name)
        return extension


# JCF Representative
class Rep(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    country = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.person.full_name}"


# JCF Employee
class Employee(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, blank=True)
    duties = models.TextField(blank=True)
    salary = models.CharField(blank=True, max_length=255, default="000")

    def __str__(self):
        return f"{self.person.full_name}"


class Appointment(models.Model):
    MODES = [("Remote", "Remote"), ("Onsite", "Onsite")]
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="appointments")
    mode = models.CharField(max_length=255, choices=MODES)
    date = models.DateField()
    done = models.BooleanField(default=False)


    def __str__(self):
        return f"Appointment: {self.person.full_name}"

    @property
    def is_today(self):
        return self.date == date.today()
