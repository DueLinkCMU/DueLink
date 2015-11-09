from mimetypes import guess_type
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden, \
    Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from datetime import datetime
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
def get_profile(request, id):
    errors = []
    # Go to the profile page of a user matching the id
    try:
        user = User.objects.get(id=id)
        profile = get_object_or_404(Profile, user=user)
        events = user.events.all()
        print profile.user.id
    except ObjectDoesNotExist:
        errors.append('This user does not exist.')
        return render(request, 'duelink/deadline_stream.html', errors)

    context = {'user': user, 'profile': profile, 'events': events, 'errors': errors}
    return render(request, 'duelink/deadline_stream.html', context)


@login_required
def get_user_image(request, id):
    profile = get_object_or_404(Profile, user=id)
    if not profile.profile_image:
        raise Http404
    content_type = guess_type(profile.profile_image.name)
    return HttpResponse(profile.profile_image, content_type=content_type)


@login_required
def get_friend_list(request):
    context = {}
    user = request.user
    friend_list = user.profile_friends.all()
    context['friend_list'] = friend_list
    return render(request, 'duelink/friend_list.html', context)


@login_required
def get_friend_stream(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    friends = User.objects.filter(profile_friends=profile)

    events = DueEvent.objects.filter(user__in=friends).order_by('deadline__due')
    return render(request, 'duelink/friend_stream.html', {'events': events})


@login_required
def add_event(request):
    if request.method == 'GET':
        form = AddEventForm()
        return render(request, 'duelink/add_event.html', {'form': form})

    if request.method == 'POST':
        form = AddEventForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            name = cleaned_data['name']
            due = cleaned_data['due']
            student = request.user
            # Use course pk to get course

            course_pk = cleaned_data['course']
            deadline = Deadline.objects.get(course=course_pk, due=due)
            # Check if the deadline exists. If not, add deadline first
            if not deadline:
                deadline = add_deadline(name, due, course_pk)

            # Then add the student to that deadline
            deadline.students.add(student)
            return redirect('home')
        else:
            return render(request, 'duelink/add_event.html', {'form': form})


@login_required
def add_deadline(name, due, course_pk):
    new_deadline = Deadline.objects.create(name=name, due=due, course=course_pk)
    new_deadline.save()
    return new_deadline

    # print("gotcha")
    # time = request.POST['deadline_time']
    # date = request.POST['deadline_date']
    # course = request.POST['deadline_course']
    # name = request.POST['deadline_name']
    # date_time = date + " " + time

    # dt = datetime.strptime(date_time, "%m/%d/%Y %H:%M")

    # new_deadline = Deadline(due=dt, course=Course.objects.get(pk=course), name=name)
    # new_deadline.save()

    # return HttpResponse("Add course success")

    # form = DeadlineForm(request.POST, instance=new_deadline)
    # print(form.errors)
    # if form.is_valid():
    #     form.save()
    # else:
    #     return HttpResponseForbidden("Add deadline fail")


@login_required
def add_course(request):
    if request.method == 'GET':
        form = CourseForm()
        return render(request, 'duelink/add_course.html', {'form': form})

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():  # Validate input data & duplicate course sections
            form.save()
            return HttpResponse("success")
        else:
            return HttpResponse("Error:" + form.errors)


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
