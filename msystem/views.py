from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
import datetime
from django.contrib import messages


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    return render(request, "msystem/clients.html")


@login_required(login_url='/login/')
def add_person(request):
    if request.method == "POST":
        # TODO: change to post
        # Get all url arguments
        full_name = request.POST["full_name"]
        dob = request.POST["date_of_birth"]
        phone = request.POST["phone"]
        telephone = request.POST["telephone"]
        profession = request.POST["profession"]
        residence = request.POST["residence"]
        country = request.POST.get("country")
        hometown = request.POST['hometown']
        religion = request.POST["religion"]
        request_info = request.POST["request_info"]
        remark = request.POST["remark"]
        solution = request.POST["solution"]
        roles = request.POST.getlist("roles")

        # parse date
        try:
            dob = datetime.datetime.strptime(dob, "%d/%m/%Y").date()
        except:
            dob=None

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

        if 'is_student' in roles: p.is_student = True
        if 'is_client' in roles: p.is_client = True
        p.save()
        messages.success(request, "Record Created Successfully")

        return HttpResponseRedirect(reverse("msystem:clients"))
    else:
        return render(request, "msystem/add_person.html")


@login_required(login_url='/login/')
def update_person(request, person_id):

    if request.method == "POST":

        # Get all POST data
        full_name = request.POST["full_name"]
        dob = request.POST["date_of_birth"]
        phone = request.POST["phone"]
        telephone = request.POST["telephone"]
        profession = request.POST["profession"]
        residence = request.POST["residence"]
        country = request.POST["country"]
        hometown = request.POST['hometown']
        religion = request.POST["religion"]
        request_info = request.POST["request_info"]
        remark = request.POST["remark"]
        solution = request.POST["solution"]
        roles = request.POST.getlist("roles")

        # parse date
        try:
            dob = datetime.datetime.strptime(dob, "%d/%m/%Y").date()
        except:
            dob = None

        # Create a model instance
        Person.objects.filter(id=person_id).update(full_name=full_name,
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
        # Get person
        p = Person.objects.get(id=person_id)

        if 'is_student' in roles: p.is_student = True
        else: p.is_student = False
        if 'is_client' in roles: p.is_client = True
        else: p.is_client = False

        p.save()

        messages.success(request, "Record Updated Successfully")

        return HttpResponseRedirect(reverse("msystem:clients"))
    else:
        # Get person
        person = Person.objects.get(id=person_id)

        try:
            dob = str(datetime.datetime.strftime(person.date_of_birth, '%d/%m/%Y'))
        except:
            dob=""

        context = {
            "update": True,
            "id": person.id,
            "full_name": person.full_name,
            "dob": dob,
            "phone": person.phone,
            "telephone": person.telephone,
            "profession": person.profession,
            "residence": person.residence,
            "country": person.country,
            "hometown": person.hometown,
            "religion": person.religion,
            "request_info": person.request_info,
            "remark": person.remark,
            "solution": person.solution,
            "is_client": person.is_client,
            "is_student": person.is_student,

        }
        print(context['dob'])
        return render(request, "msystem/add_person.html", context)

@login_required(login_url='/login/')
def clients(request):
    p = Person.objects.filter(is_client=True).order_by("id")

    # if there's a search query, filter p
    if "q" in request.GET:
        q = request.GET['q']
        print("====================================================")
        p = Person.objects.filter(is_client=True).filter(full_name__icontains=q).order_by("id")

    context = {
        "clients": p,
    }
    return render(request, "msystem/clients.html", context)


def client_profile(request, client_id):
    p = Person.objects.get(id=client_id)

    context = {
        'client': p,
    }

    return render(request, 'msystem/client_profile.html', context)


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