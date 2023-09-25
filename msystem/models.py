from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Profile(models.Model):
    role_choices = [
        ("admin", "Admin"),
        ("administrator", "Administrator"),
        ("secretary", "Secretary"),
        ("media_operations", "Media Operations")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    phone = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=role_choices)

    def __str__(self):
        return f"{self.user.username}"


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
    referral = models.CharField(max_length=255, blank=True)
    is_client = models.BooleanField(blank=True, default=True)
    is_student = models.BooleanField(default=False)
    is_advanced_student = models.BooleanField(default=False)

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

    @property
    def filesize(self):
        x = self.file.size
        y = 512000
        if x < y:
            value = round(x / 1000, 2)
            ext = ' kb'
        elif x < y * 1000:
            value = round(x / 1000000, 2)
            ext = ' MB'
        else:
            value = round(x / 1000000000, 2)
            ext = ' GB'
        return str(value) + ext


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

    # class Meta:
    #     unique_together = ["person", "date"]

    def __str__(self):
        return f"Appointment: {self.person.full_name}"

    @property
    def is_today(self):
        return self.date == date.today()


class Request(models.Model):
    person = models.ForeignKey(Person, related_name="requests", on_delete=models.CASCADE)
    request_info = models.TextField(blank=True)
    remark = models.TextField(blank=True)
    solution = models.TextField(blank=True)

    def __str__(self):
        return f"Request: {self.person.full_name}"


# ========================== Media ========================================
class MediaTopic(models.Model):
    type_choices = [
        ("lecture", "Lecture"),
        ("interview", "interview"),
        ("live", "Live"),
        ("documentary", "Documentary"),
        ("promotional", "Promotional")
    ]

    status_choices = [
        ("pending", "Pending"),
        ("archive", "Archive"),
        ("published", "Published")
    ]

    language_choices = [
        ("english", "English"),
        ("twi", "Twi"),
    ]

    topic = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=50, choices=type_choices, default="lecture")
    language = models.CharField(max_length=50, default="english")
    status = models.CharField(max_length=50, choices=status_choices, default="pending")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.topic}"
