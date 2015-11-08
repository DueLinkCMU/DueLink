from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.db import transaction
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login, authenticate, logout
from forms import *
from models import *


# Create your views here.


@ensure_csrf_cookie
@login_required
def home(request):
    # Display the global posts of all users
    if request.method == 'GET':
        context = {}
        response = render(request, 'DueLink/home.html', context)
        return response


@login_required
def profile(request):
    return HttpResponse("This is profile page")


@login_required
def get_user_image(request):
    return HttpResponse("This is for get user image")


@login_required
def add_deadline(request):
    if request.method == 'GET':
        form = DeadlineForm()
        return render(request, 'duelink/add_deadline.html', {'form': form})

    if request.method == 'POST':
        form = DeadlineForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse("Add deadline fail")


@login_required
def add_course(request):
    if request.method == 'GET':
        form = CourseForm()
        return render(request, 'duelink/add_course.html', {'form': form})

    if request.method == 'POST':
        school = request.POST['school']
        a = request.POST['section']
        print(a.strlen)

        new_course = Course(school=School.objects.get(pk=school), section=a)
        form = CourseForm(request.POST, instance=new_course)
        form.is_valid()



@transaction.atomic
def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'duelink/register.html', {'form': form})

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            print("invalid")
            return render(request, 'duelink/register.html', {'form': form})

        new_user = User.objects.create_user(username=form.clean_username(), email=form.clean_email(),
                                            password=form.cleaned_data['password1'])
        new_user.save()

        info = {'nick_name': form.cleaned_data['nick_name'],
                'school': School.objects.get(name="central michigan univ").pk}  # TODO: school name

        # TODO: school exist?

        new_profile = Profile(user=new_user)
        profile_form = ProfileForm(info, instance=new_profile)

        if profile_form.is_valid():
            profile_form.save()
        else:
            return HttpResponseRedirect("Not good")

        login_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(request, login_user)

    return HttpResponseRedirect(reverse('home'))
