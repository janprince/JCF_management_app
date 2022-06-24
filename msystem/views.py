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
    return HttpResponseRedirect(reverse("msystem:clients"))


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
        gender = request.POST['gender']
        referral = request.POST['referral']
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
                   gender=gender,
                   telephone=telephone,
                   profession=profession,
                   residence=residence,
                   country=country,
                   hometown=hometown,
                   referral=referral,
                   religion=religion,
                   request_info=request_info,
                   remark=remark,
                   solution=solution
            )

        if 'is_student' in roles: p.is_student = True
        if 'is_client' in roles: p.is_client = True
        p.save()

        # check for uploaded files
        if request.FILES:
            print("==========================================================")
            print(request.FILES)
            files = request.FILES.getlist('datafile')  # since upload could be multiple
            for file in files:
                print(file)
                d = DataFile(person=p, file=file)
                d.save()

        messages.success(request, "Record Created Successfully")

        return HttpResponseRedirect(reverse("msystem:clients"))
    else:
        return render(request, "msystem/modify_person.html")


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
        gender = request.POST['gender']
        referral = request.POST['referral']
        request_info = request.POST["request_info"]
        remark = request.POST["remark"]
        solution = request.POST["solution"]
        roles = request.POST.getlist("roles")

        # parse date
        try:
            dob = datetime.datetime.strptime(dob, "%d/%m/%Y").date()
        except:
            dob = None

        # Update a model instance
        Person.objects.filter(id=person_id).update(
            full_name=full_name,
            phone=phone,
            date_of_birth=dob,
            telephone=telephone,
            gender=gender,
            referral=referral,
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

        # check for uploaded files
        if request.FILES:
            print("==========================================================")
            print(request.FILES)
            files = request.FILES.getlist('datafile')       # since upload could be multiple
            for file in files:
                print(file)
                d = DataFile(person=p, file=file)
                d.save()

        # feedback
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
            "person": person,
            "dob": dob,

        }
        return render(request, "msystem/modify_person.html", context)


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


@login_required(login_url='/login/')
def client_profile(request, client_id):
    p = Person.objects.get(id=client_id)
    p_appointments = p.appointments.filter(done=False)
    print(p_appointments)

    context = {
        'client': p,

    }

    return render(request, 'msystem/client_profile.html', context)


def delete_client(request, client_id):
    c = Person.objects.get(id=client_id)
    try:
        c.delete()
        # feedback
        messages.success(request, f"{c.full_name} deleted")
    except:
        messages.warning(request, f"Deletion Failed")

    return HttpResponseRedirect(reverse("msystem:clients"))


@login_required(login_url='/login/')
def students(request):
    studs = Person.objects.filter(is_student=True).order_by("id")

    # if there's a search query, filter p
    if "q" in request.GET:
        q = request.GET['q']
        print("====================================================")
        studs = Person.objects.filter(is_student=True).filter(full_name__icontains=q).order_by("id")

    context = {
        "clients": studs,
        "page": "students"
    }
    return render(request, "msystem/students.html", context)
    pass


def book_client(request, client_id):
    client = Person.objects.get(id=client_id)

    if request.method == "POST":
        appointment_date = request.POST["appointment_date"]
        mode = request.POST["mode"]

        # parse date
        try:
            appointment_date = datetime.datetime.strptime(appointment_date, "%d/%m/%Y").date()
        except:
            appointment_date = None

        a = Appointment(person=client, mode=mode, date=appointment_date)
        a.save()

        # feedback
        messages.success(request, "Appointment Booked Successfully")

        return HttpResponseRedirect(reverse("msystem:appointments"))

    context = {
        "client": client,
    }

    return render(request, "msystem/book_client.html", context)


def appointments(request):
    a = Appointment.objects.filter(done=False).order_by("id")

    # if there's a search query, filter p
    if "q" in request.GET:
        q = request.GET['q']
        print("====================================================")
        a = Appointment.objects.filter(done=False, person__full_name__icontains=q).order_by("id")

    context = {
        "appointments": a,
    }
    return render(request, "msystem/appointments.html", context)


def change_appointment(request, ap_id):
    ap = Appointment.objects.get(id=ap_id)
    client = ap.person

    if request.method == "POST":
        appointment_date = request.POST["appointment_date"]
        mode = request.POST["mode"]

        # parse date
        try:
            appointment_date = datetime.datetime.strptime(appointment_date, "%d/%m/%Y").date()
        except:
            appointment_date = None

        Appointment.objects.filter(id=ap_id).update(
            mode=mode,
            date=appointment_date
        )

        # feedback
        messages.success(request, "Appointment Updated Successfully")

        return HttpResponseRedirect(reverse("msystem:appointments"))

    try:
        ap_date = str(datetime.datetime.strftime(ap.date, '%d/%m/%Y'))
    except:
        ap_date = ""

    context = {
        "appointment": ap,
        "ap_date": ap_date,
        "client": client,
    }

    return render(request, "msystem/book_client.html", context)


def delete_appointment(request, ap_id):
    a = Appointment.objects.get(id=ap_id)

    try:
        a.delete()
        # feedback
        messages.success(request, f"Appointment with {a.person.full_name} deleted")
    except:
        messages.warning(request, f"Deletion Failed")

    return HttpResponseRedirect(reverse("msystem:appointments"))


def mark_appointment(request, ap_id):
    a = Appointment.objects.get(id=ap_id)
    a.done = True
    a.save()

    messages.success(request, f"Appointment #{ap_id} marked complete")

    return HttpResponseRedirect(reverse("msystem:appointments"))




def login_view(request):
    if request.method == "POST":
        email = request.POST.get("useremail")
        password = request.POST.get("password")
        user = User.objects.get(email=email)
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return HttpResponseRedirect(reverse("msystem:clients"))
        else:
            messages.warning(request, "Invalid email or password")
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