from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
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
def get_friend_list(request):
    context = {}
    user = request.user
    friend_list = user.profile_friends.all()
    context['friend_list'] = friend_list
    return render(request, 'duelink/friend_list.html', context)


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
        print(a)

        new_course = Course(school=School.objects.get(pk=school), section=a)
        form = CourseForm(request.POST, instance=new_course)
        if form.is_valid():
            form.save()


def add_school(request):
    if request.method == 'GET':
        form = SchoolForm()
        return render(request, 'duelink/add_school.html', {'form': form})

    if request.method == 'POST':
        form = SchoolForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse("save school")
        else:
            return HttpResponseForbidden("fail")


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
                'school': School.objects.get(name=form.cleaned_data['school']).pk}  # TODO: school name

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


@login_required
@transaction.atomic
def edit_profile(request):
    user = request.user
    profile_to_edit = get_object_or_404(Profile, user=user)
    user_to_to_edit = get_object_or_404(User, id=user.id)

    context = {}
    if request.method == 'GET':
        user_form = UserForm(instance=user_to_to_edit)
        profile_form = EditProfileForm(instance=profile_to_edit)  # Creates form from the
        context = {'profile_form': profile_form,
                   'user_form': user_form}  # profile_to_edit)
        return render(request, 'duelink/edit_profile.html', context)

    # if method is POST, get form data to update the model
    user_form = UserForm(request.POST, instance=user_to_to_edit)
    profile_form = EditProfileForm(request.POST, request.FILES, instance=profile_to_edit)
    context['profile_form'] = profile_form
    context['user_form'] = user_form

    if not profile_form.is_valid() or not user_form.is_valid():
        return render(request, 'duelink/edit_profile.html', context)
    user_form.save()
    profile_form.save()

    return redirect('profile', user.id)
