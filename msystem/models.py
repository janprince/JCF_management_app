from django.db import models


# Person
class Person(models.Model):
    date_added = models.DateField(auto_now_add=True)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True)
    contact = models.IntegerField(max_length=255)
    telephone = models.IntegerField(max_length=255, blank=True)
    religion = models.CharField(max_length=255, default="N/A")
    residence = models.CharField(max_length=255, blank=True)
    hometown = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255)
    region = models.CharField(max_length=255, blank=True)
    f_name = models.CharField(max_length=255, blank=True)
    m_name = models.CharField(max_length=255, blank=True)
    request_info = models.TextField(blank=True)
    remark = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    # jcf_member = models.BooleanField()
    client = models.BooleanField(blank=True)
    student = models.BooleanField(blank=True)
    employee = models.BooleanField(blank=True)
    rep = models.BooleanField(blank=True)

    def __str__(self):
        return f"{self.full_name}"


# JCF Representative
class Rep(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    country = models.CharField(max_length=255)
    region = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.person.full_name}"


# JCF Employee
class Employee(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    salary = models.IntegerField()

    def __str__(self):
        return f"{self.person.full_name}"


class Booking(models.Model):
    MODES = [("REMOTE", "Remote"), ("ONSITE", "Onsite")]
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="bookings")
    modes = models.CharField(max_length=255, choices=MODES)
    date = models.DateField()

