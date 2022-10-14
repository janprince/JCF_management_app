from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
import datetime
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import  Group


# =========================== Dashboards ========================================
@login_required(login_url='/login/')
def analytics(request):
    clients_count = Person.objects.filter(is_client=True).count()
    students_count = Person.objects.filter(is_student=True).count()
    appointments_count = Appointment.objects.filter(done=False).count()

    context = {
        "client_count": clients_count,
        "student_count": students_count,
        "appointment_count": appointments_count,
    }
    return render(request, "msystem/dash/analytics.html", context)


@login_required(login_url='/login/')
def finance(request):
    pass


@login_required(login_url='/login/')
def index(request):
    return HttpResponseRedirect(reverse("msystem:analytics"))


@login_required(login_url='/login/')
def add_person(request):
    """
    Add a new person to the system
    """
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

        # handling errors - duplicate Person instance
        try:
            p.save()
        except IntegrityError:
            messages.warning(request, "Profile Already Exists")
            return HttpResponseRedirect(reverse("msystem:clients"))

        # add_datafiles
        add_datafiles(request, p)

        messages.success(request, "Record Created Successfully")

        return HttpResponseRedirect(reverse("msystem:clients"))
    else:
        return render(request, "msystem/forms/add_client.html")


# ========= DataFiles ===========
def add_datafiles(request, person):
    # check if request object comes with any uploaded files
    if request.FILES:
        print("==========================================================")
        print(request.FILES)
        files = request.FILES.getlist('datafile')  # since upload could be multiple
        for file in files:
            print(file)
            d = DataFile(person=person, file=file)
            d.save()


def add_client_files(request, person_id):
    """Add additional files to a client"""

    person = Person.objects.get(id=person_id)

    if request.method == "POST":
        add_datafiles(request, person)

    return HttpResponseRedirect(reverse("msystem:client_profile", args=(person_id,)))


@login_required(login_url='/login/')
def update_person(request, person_id):
    """
    Update a person's details
    """
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

        # add datafiles
        add_datafiles(request, p)

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
        return render(request, "msystem/forms/add_client.html", context)


@login_required(login_url='/login/')
def clients(request):
    p = Person.objects.filter(is_client=True).order_by("-id")

    # if there's a search query, filter p
    if "q" in request.GET:
        q = request.GET['q']
        print("====================================================")
        p = Person.objects.filter(is_client=True).filter(full_name__icontains=q).order_by("id")

    context = {
        "clients": p,
    }
    return render(request, "msystem/datatables/clients.html", context)


@login_required(login_url='/login/')
def client_profile(request, client_id):
    p = Person.objects.get(id=client_id)

    # get client's appointment due toady, if any;
    try:
        p_appointment = p.appointments.get(done=False, date=date.today())
    except:
        p_appointment = None
    print(p_appointment)

    context = {
        'client': p,
        'client_has_appointment': p_appointment
    }

    return render(request, 'msystem/client_profile2.html', context)


@login_required(login_url='/login/')
def delete_client(request, client_id):
    """
    Delete a client
    """
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
    """
    Renders all students
    """
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
    return render(request, "msystem/datatables/students.html", context)
    pass


# ================================= Appointments =================================
@login_required(login_url='/login/')
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

        try:
            a = Appointment(person=client, mode=mode, date=appointment_date)
            a.save()
        except IntegrityError:
            messages.warning(request, "Appointment already exists.")
            return HttpResponseRedirect(reverse("msystem:appointments"))

        # feedback
        messages.success(request, "Appointment Booked Successfully")

        return HttpResponseRedirect(reverse("msystem:appointments"))

    context = {
        "client": client,
    }

    return render(request, "msystem/forms/add_appointment.html", context)


@login_required(login_url='/login/')
def appointments(request):
    a = Appointment.objects.filter(done=False).order_by("id")
    # a = Appointment.objects.filter(date__gte=date.today()).order_by('id')

    # if there's a search query, filter a
    if "q" in request.GET:
        q = request.GET['q']
        a = Appointment.objects.filter(done=False, person__full_name__icontains=q).order_by("id")

    context = {
        "appointments": a,
    }
    return render(request, "msystem/datatables/appointments.html", context)


@login_required(login_url='/login/')
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

    return render(request, "msystem/forms/add_appointment.html", context)


@login_required(login_url='/login/')
def delete_appointment(request, ap_id):
    a = Appointment.objects.get(id=ap_id)

    try:
        a.delete()
        # feedback
        messages.success(request, f"Appointment with {a.person.full_name} deleted")
    except:
        messages.warning(request, f"Deletion Failed")

    return HttpResponseRedirect(reverse("msystem:appointments"))


@login_required(login_url='/login/')
def mark_appointment(request, ap_id):
    """
    Mark an appointment as done
    """
    a = Appointment.objects.get(id=ap_id)
    a.done = True
    a.save()

    messages.success(request, f"Appointment #{ap_id} marked complete")

    return HttpResponseRedirect(reverse("msystem:appointments"))


# ================================ Employees ===================================
@login_required(login_url='/login/')
def employees(request):
    userGroup = Group.objects.get(user=request.user).name
    if userGroup == 'admin':
        emps = Employee.objects.all()
        context = {
            "employees": emps,
        }
    elif userGroup == 'staff':
        notallowed = True
        context = {
            "notallowed": notallowed,
        }


    # if there's a search query, filter p
    if "q" in request.GET:
        q = request.GET['q']
        emps = Employee.objects.filter(person__full_name__icontains=q).order_by("id")


    return render(request, "msystem/datatables/employees.html", context)


@login_required(login_url='/login/')
def add_employee(request, person_id):
    person = Person.objects.get(id=person_id)

    if request.method == "POST":
        role = request.POST["role"]
        duties = request.POST["duties"]
        salary = request.POST["salary"]

        emp = Employee(person=person, role=role, duties=duties, salary=salary)
        emp.save()

        # feedback
        messages.success(request, "Employee Added")

        return HttpResponseRedirect(reverse("msystem:employees"))

    context = {
        "person": person,
    }

    return render(request, "msystem/forms/add_employee.html", context)


@login_required(login_url='/login/')
def update_employee(request, emp_id):
    emp = Employee.objects.get(id=emp_id)
    person = emp.person

    if request.method == "POST":
        role = request.POST["role"]
        duties = request.POST["duties"]
        salary = request.POST["salary"]

        Employee.objects.filter(id=emp_id).update(
            role=role,
            duties=duties,
            salary=salary,
        )

        # feedback
        messages.success(request, f"Employee #{emp.id} Updated")

        return HttpResponseRedirect(reverse("msystem:employees"))

    context = {
        "employee": emp,
        "person": person,
    }

    return render(request, "msystem/forms/add_employee.html", context)


# ========================= Accounts Management ================================
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("emailaddress")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except:
            user = None
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return HttpResponseRedirect(reverse("msystem:analytics"))
        else:
            messages.error(request, "Invalid email or password. Please try Again.")
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