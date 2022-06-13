from django.db import models


# Person
class Person(models.Model):
    date_added = models.DateField(auto_now_add=True)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=255)
    profession = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    religion = models.CharField(max_length=255, default="N/A")
    residence = models.CharField(max_length=255, blank=True)
    hometown = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, default="Ghana")
    region = models.CharField(max_length=255, blank=True)
    f_name = models.CharField(max_length=255, blank=True)
    m_name = models.CharField(max_length=255, blank=True)
    request_info = models.TextField(blank=True)
    remark = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    # jcf_member = models.BooleanField()
    is_client = models.BooleanField(blank=True, default=True)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name}"


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
    salary = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.person.full_name}"


class Booking(models.Model):
    MODES = [("REMOTE", "Remote"), ("ONSITE", "Onsite")]
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="bookings")
    modes = models.CharField(max_length=255, choices=MODES)
    date = models.DateField()

