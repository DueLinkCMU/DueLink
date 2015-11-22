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
        user = get_object_or_404(User, id=id)
        self = (user == request.user)
        profile_page = True
        profile = get_object_or_404(Profile, user=user)
        events = user.events.all()
        print profile.user.id
    except ObjectDoesNotExist:
        errors.append('This user does not exist.')
        return render(request, 'duelink/deadline_stream.html', errors)

    profile_me = get_object_or_404(Profile, user = request.user)
    linked = profile_me.friends.filter(id = id).exists()

    context = {'user': user, 'profile': profile, 'events': events, 'errors': errors, 'profile_page': profile_page,
               'self': self, 'user_id':id, 'linked':linked}

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
    profile_page = False
    self = False
    events = DueEvent.objects.filter(user__in=friends).order_by('-deadline__due')
    context = {'events': events, 'profile_page': profile_page, 'self': self}
    return render(request, 'duelink/friend_stream.html', context)


@login_required
def add_event(request):
    if request.method == 'GET':
        form = AddEventForm()
        return render(request, 'duelink/add_event.html', {'form': form})

    if request.method == 'POST':
        form = AddEventForm(request.POST)
        if form.is_valid():
            deadline = form.clean_deadline(request)  # Check and return dl .Ee suppose user create event for themselves
            if not deadline:
                return HttpResponseForbidden("Fail to add event: Duplicated event")

            student = request.user
            deadline.students.add(student)

            # Then add the student to that deadline
            new_event = DueEvent.objects.create(deadline=deadline, user=student)
            new_event.save()
            return HttpResponse("Successfully add event")
        else:
            return HttpResponseForbidden("Fail to add event")


@login_required
def add_deadline(request, name, due, course_pk):
    new_deadline = Deadline.objects.create(name=name, due=due, course=course_pk)
    print("step1")
    new_deadline.save()
    print("step2")
    return new_deadline


@transaction.atomic
@login_required
def add_task(request, event_id=None):
    event = get_object_or_404(DueEvent, id=event_id)
    if request.method == 'GET':
        form = TaskForm()
        return render(request, 'duelink/add_task.html', {'task_form': form, 'event_id': event_id})

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if not event_id:
            return Http404
        if form.is_valid():
            task = form.save(commit=False)
            task.event = event
            task.save()
            # return HttpResponseRedirect('tasks', event_id)
            # return redirect('profile', request.user.id)

            return redirect('get_tasks',event_id)
        else:
            print form
            return HttpResponseForbidden("Error:" + form.__str__())
    return Http404


@login_required
def get_tasks(request, event_id=None):
    event = get_object_or_404(DueEvent, id=event_id)
    if request.method == 'GET':
        tasks = event.tasks.all()
        return render(request, 'duelink/tasks.html', {'tasks': tasks,'event':event})


@login_required
@transaction.atomic
def update_task(request, task_id=None):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'GET':
        return render(request, 'duelink/task_form.html',
                      {'task_form':UpdateTaskForm(),'task': task})

    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        if task.finished:
            task.finished = False
        else:
            task.finished = True
        task.save()
        return redirect('get_tasks',task.event.id)
        # form = UpdateTaskForm(request.POST, instance=task)
        #
        # if form.is_valid():
        #     form.save()
        #     return redirect('get_tasks',task.event.id)
        # else:
        #     print form
        #     return HttpResponse("Error" + form.__str__())


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


@login_required
def display_tasks(request, event_id):
    tasks = Task.objects.filter(event=event_id)
    context = {tasks}
    return render(request, 'duelink/tasks.html', context)

@transaction.atomic
@login_required
def link(request,user_id):
    user_ = get_object_or_404(User,id=user_id)
    profile = get_object_or_404(Profile, user=request.user)
    profile_ = get_object_or_404(Profile, user=user_)
    if request.method == "POST":

        profile.friends.add(user_)
        profile.save()
        profile_.friends.add(request.user)
        profile.save()
        return HttpResponse("success")

    return Http404

@transaction.atomic
@login_required
def unlink(request,user_id):
    user_ = get_object_or_404(User,id=user_id)
    profile = get_object_or_404(Profile, user=request.user)
    profile_ = get_object_or_404(Profile, user = user_)
    if request.method == "POST":
        profile.friends.remove(user_)
        profile.save()
        profile_.friends.remove(request.user)
        profile_.save()
        return HttpResponse("success")

    return Http404