from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.dateparse import parse_date
from .models import *


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    return render(request, "msystem/add_person.html")


def add_person(request):
    if request.method == "GET":
        print(request.GET)
        full_name = request.GET["name"]
        dob = request.GET["dob"]
        phone = request.GET["phone"]
        telephone = request.GET["telephone"]
        profession = request.GET["profession"]
        residence = request.GET["name"]
        country = request.GET["country"]
        hometown = request.GET['hometown']
        religion = request.GET["religion"]
        request_info = request.GET["request_info"]
        remark = request.GET["remark"]
        solution = request.GET["solution"]
        roles = request.GET.getlist("roles")

        # parse date
        dob = parse_date(dob)

        # Create a model instance
        p = Person(full_name=full_name,
                   phone=phone,
                   date_of_birth=dob,
                   telephone=telephone,
                   profession=profession,
                   residence=residence,
                   country=country,
                   hometown=hometown,
                   religion=religion,
                   request_info=request_info,
                   remark=remark,
                   solution=solution
            )

        if 'student' in roles: p.is_student = True
        if 'employee' in roles: p.is_employee = True
        if 'client' in roles: p.is_client = True
        if 'rep' in roles: p.is_rep = True
        p.save()

        if 'employee' in roles:
            # create new employee
            e = Employee(person=p)
            e.save()

        if 'rep' in roles:
            # create new rep
            r = Rep(person=p)
            r.save()
        return render(request, "msystem/add_client.html")
    else:
        return render(request, "msystem/add_client.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("useremail")
        password = request.POST.get("password")
        user = User.objects.get(email=email)
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("msystem:index"))
        else:
            context = {
                'error': "Invalid email or password",
            }
            return render(request, "msystem/login.html", context=context)
    return render(request, "msystem/login.html")


def signup(request):
    return render(request, "msystem/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("msystem:login"))