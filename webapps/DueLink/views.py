from mimetypes import guess_type
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden, \
    Http404
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from datetime import datetime
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login, authenticate, logout
from DueLink.forms import *
from DueLink.models import *


# Create your views here.


@ensure_csrf_cookie
@login_required
def home(request):
    # Display the global posts of all users
    if request.method == 'GET':
        context = {}
        response = render(request, 'duelink/home.html', context)
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
        events = user.events.filter(deadline__due__gt=datetime.now())
        events_dued = DueEvent.objects.filter(deadline__due__lte=datetime.now()).order_by('-deadline__due')
        teams = user.teams.all()
        events_team = DueEvent.objects.filter(team__in=teams).filter(deadline__due__gt=datetime.now())
        events_team_dued = DueEvent.objects.filter(team__in=teams).filter(deadline__due__lte=datetime.now())
        events = events | events_team
        events.order_by('deadline__due')
        events_dued = events_dued | events_team_dued
        events_dued.order_by('deadline__due')
        # (profile.user.id)
    except ObjectDoesNotExist:
        errors.append('This user does not exist.')
        return render(request, 'duelink/deadline_stream.html', errors)

    profile_me = get_object_or_404(Profile, user=request.user)
    linked = profile_me.friends.filter(id=id).exists()

    context = {'user': user, 'profile': profile, 'events': events, 'events_dued': events_dued, 'errors': errors,
               'profile_page': profile_page, 'self': self, 'user_id': id, 'linked': linked}
    if self:
        num_of_course = Course.objects.filter(students=user).count()
        context['num_of_course'] = num_of_course

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
    context['recommend_list'] = recommend_friends(user)
    return render(request, 'duelink/friend_list.html', context)


def recommend_friends(user):
    profile = get_object_or_404(Profile, user=user)
    courses = profile.get_courses
    friends = profile.friends
    recommendations = {}
    for course in courses:
        for student in course.students.all():
            if student not in friends.all() and student != user:
                recommendations[student] = course.course_number
                if len(recommendations) == 10:
                    break
    return recommendations


@login_required
def get_friend_stream(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    friends = User.objects.filter(profile_friends=profile)
    profile_page = False
    self = False
    events = DueEvent.objects.filter(user__in=friends).filter(deadline__due__gt=datetime.now()).order_by(
        'deadline__due')
    events_dued = DueEvent.objects.filter(user__in=friends).filter(deadline__due__lte=datetime.now()).order_by(
        '-deadline__due')
    context = {'events': events, 'events_dued': events_dued, 'profile_page': profile_page, 'self': self}
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
    new_deadline.save()
    return new_deadline


@transaction.atomic
@login_required
def add_task(request):
    context = {}
    # if not request.POST['event_id']:
    if 'event_id' not in request.POST:
        raise Http404

    form = TaskForm(request.POST)
    event_id = request.POST['event_id']
    # print(request.POST)
    event = get_object_or_404(DueEvent, id=event_id)

    if form.is_valid():
        new_task = Task.objects.create(description=form.cleaned_data['description'],
                                       event=event)
        new_task.save()
        # Add the new task to page
        context['task'] = new_task
        response = render(request, 'duelink/task.json', context, content_type="application/json")
        return response
    else:
        # Return errors
        context['event'] = event
        context["form"] = form
        response = render(request, 'duelink/new_task_form.json', context, content_type='application/json')
        return response


@login_required
def get_tasks(request, event_id=None):
    event = get_object_or_404(DueEvent, id=event_id)
    if request.method == 'GET':
        task_form = TaskForm()
        tasks = event.tasks.all()
        return render(request, 'duelink/tasks.html',
                      {'tasks': tasks, 'task_form': task_form, 'event': event, 'event_id': event_id})


@login_required
@transaction.atomic
def update_task(request, task_id=None):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'GET':
        return render(request, 'duelink/task_form.html',
                      {'task_form': UpdateTaskForm(), 'task': task})

    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)

        if task.finished:
            task.finished = False

        else:
            task.finished = True
        task.save()
        response = render(request, 'duelink/task.json', {"task": task}, content_type="application/json")
        return response

    return HttpResponseForbidden("Error")


@login_required
@transaction.atomic
def delete_task(request, task_id=None):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return HttpResponse("OK")
    return HttpResponseForbidden("Error")


@login_required
@transaction.atomic
def add_course(request):
    if request.method == 'GET':
        form = AddCourseForm()
        return render(request, 'duelink/add_course.html', {'form': form})

    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():  # Validate input data & duplicate course sections
            form.save()
            return HttpResponse("success")
        else:
            return HttpResponse(form.errors)


def add_school(request):
    if request.method == 'GET':
        form = AddSchoolForm()
        return render(request, 'duelink/add_school.html', {'form': form})

    if request.method == 'POST':
        form = AddSchoolForm(request.POST)

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
def display_tasks(request, event_id):
    tasks = Task.objects.filter(event=event_id)
    context = {tasks}
    return render(request, 'duelink/tasks.html', context)


@transaction.atomic
@login_required
def link(request, user_id):
    user_ = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=request.user)
    profile_ = get_object_or_404(Profile, user=user_)
    if request.method == "POST":
        profile.friends.add(user_)
        profile.save()
        profile_.friends.add(request.user)
        profile.save()
        return HttpResponse("success link")

    return HttpResponseForbidden


@transaction.atomic
@login_required
def unlink(request, user_id):
    user_ = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=request.user)
    profile_ = get_object_or_404(Profile, user=user_)
    if request.method == "POST":
        profile.friends.remove(user_)
        profile.save()
        profile_.friends.remove(request.user)
        profile_.save()
        return HttpResponse("success unlink")

    return HttpResponseForbidden


@login_required
def search_people(request):
    if not 'search_term' in request.POST:
        return HttpResponseForbidden("Not a valid request")
    name = request.POST['search_term']
    result_username = Profile.objects.filter(user__in=User.objects.filter(username__icontains=name))
    result_nickname = Profile.objects.filter(nick_name__icontains=name)
    result_join = result_username | result_nickname

    if result_join.count() == 0:
        context = {'search_result': 'Sorry, can\'t find such user.'}
        return render(request, 'duelink/404.html', context)

    context = {'friend_list': result_join, 'search_result': True, 'search_term': name}
    return render(request, 'duelink/friend_list.html', context)


@login_required
def search_course(request):
    # return a courses.json
    context = {'courses': Course.objects.all()}
    if request.method == "GET":
        return render(request, 'duelink/courses.json', context, content_type="application/json")


@login_required
def display_user_course(request):
    user = request.user
    skim = False
    if 'skim' in request.POST:
        if request.POST['skim'] == '1':
            skim = True

    courses = Course.objects.filter(students=user)

    context = {'courses': courses, 'skim': skim}
    return render(request, 'duelink_json/display_user_course.json', context, content_type='application/json')


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
                   'user_form': user_form, 'edit_profile': True}  # profile_to_edit)
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
@transaction.atomic
def subscribe_course(request):
    if request.method == 'GET':
        form = SubscribeCourseForm()
        context = {'subscribe_course_form': form, 'subscribe_course': True}
        return render(request, 'duelink/subscribe_course.html', context)

    if request.method == 'POST':
        form = SubscribeCourseForm(request.POST)
        if form.is_valid() and form.clean_exist(request.user):
            course = form.cleaned_data['course']
            course.students.add(request.user)
            context = {'courses': [course, ]}
            return render(request, 'duelink_json/display_user_course.json', context, content_type='application/json')
        else:
            return HttpResponseForbidden("Invalid or subscribed course")


@transaction.atomic
@login_required
def add_team(request):
    if request.method == "GET":
        context = {'form': AddTeamForm}
        return render(request, 'duelink/add_team.html', context)
    if request.method == "POST":
        form = AddTeamForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            course_pk = form.cleaned_data['course']
            team = Team.objects.create(creator=request.user, name=name, course=course_pk)
            team.members.add(request.user)
            team.save()
            return HttpResponse("success link")

    return HttpResponseForbidden


@transaction.atomic
@login_required
def add_member(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == "POST":
        user_id = request.POST['member']
        user = get_object_or_404(User, id=user_id)
        team.members.add(user)
        team.save()
        return HttpResponse("success link")

    return HttpResponseForbidden


@transaction.atomic
@login_required
def remove_member(request, team_id):
    user_ = get_object_or_404(User, id=team_id)
    profile = get_object_or_404(Profile, user=request.user)
    profile_ = get_object_or_404(Profile, user=user_)
    if request.method == "POST":
        profile.friends.add(user_)
        profile.save()
        profile_.friends.add(request.user)
        profile.save()
        return HttpResponse("success link")

    return HttpResponseForbidden


@login_required
def get_team_list(request):
    context = {}
    user = request.user
    team_list = user.profile_friends.all()
    context['team_list'] = team_list
    return render(request, 'duelink/team_list.html', context)


@login_required
def get_team_stream(request):
    errors = []
    try:
        user = request.user
        self = True
        profile_page = True
        teams = user.teams.all()
        profile = get_object_or_404(Profile, user=user)
        events = DueEvent.objects.filter(team__in=teams).filter(deadline__due__gt=datetime.now()).order_by(
            'deadline__due')
        events_dued = DueEvent.objects.filter(team__in=teams).filter(deadline__due__lte=datetime.now()).order_by(
            '-deadline__due')
    except ObjectDoesNotExist:
        errors.append('This user does not exist.')
        return render(request, 'duelink/deadline_stream.html', errors)

    profile_me = get_object_or_404(Profile, user=request.user)
    linked = False
    context = {'user': user, 'profile': profile, 'events': events, 'events_dued': events_dued, 'errors': errors,
               'profile_page': profile_page, 'self': self, 'user_id': id, 'linked': linked, 'isTeams': True,
               'teams': teams, 'team_num': len(teams)}

    if self:
        num_of_course = Course.objects.filter(students=user).count()
        context['num_of_course'] = num_of_course

    return render(request, 'duelink/deadline_stream.html', context)


@login_required
def get_team_stream_by_id(request, team_id):
    errors = []
    try:
        user = request.user
        team = get_object_or_404(Team, id=team_id)
        teams = user.teams.all()
        self = (user in team.members.all())
        profile_page = True
        profile = get_object_or_404(Profile, user=user)
        events = team.events.filter(deadline__due__gt=datetime.now()).order_by('deadline__due')
        events_dued = team.events.filter(deadline__due__lte=datetime.now()).order_by('-deadline__due')
        form = AddMemberForm(user=user)

    except ObjectDoesNotExist:
        errors.append('This user does not exist.')
        return render(request, 'duelink/deadline_stream.html', errors)

    profile_me = get_object_or_404(Profile, user=request.user)
    linked = False

    context = {'user': user, 'profile': profile, 'events': events, 'events_dued': events_dued, 'errors': errors,
               'profile_page': profile_page, 'self': self, 'user_id': id, 'linked': linked, 'isTeam': True,
               'team': team, 'teams': teams, 'form': form, 'member_num': len(team.members.all()),
               'team_num': len(teams)}

    if self:
        num_of_course = Course.objects.filter(students=user).count()
        context['num_of_course'] = num_of_course

    return render(request, 'duelink/deadline_stream.html', context)


@login_required
@transaction.atomic
def add_event_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'GET':
        form = AddEventForm({'course': team.course.id})
        return render(request, 'duelink/add_event.html', {'form': form, 'isTeam': True, 'team_id': team_id})

    if request.method == 'POST':
        form = AddEventForm(request.POST)
        if form.is_valid():
            deadline = form.clean_deadline(request)  # Check and return dl .Ee suppose user create event for themselves
            if not deadline:
                return HttpResponseForbidden("Fail to add event: Duplicated event")

            student = request.user
            deadline.students.add(student)

            # Then add the student to that deadline
            new_event = DueEvent.objects.create(deadline=deadline, user=student, team=team)
            new_event.save()
            return HttpResponse("Successfully add event")
        else:
            return HttpResponseForbidden("Fail to add event")


def unsubscribe_course(request):
    if request.method == 'POST':
        form = UnsubscribeCourseForm(request.POST)
        if form.is_valid() and form.valid_user(request.user):
            print(form.cleaned_data['course_id'])
            course = Course.objects.get(id=form.cleaned_data['course_id'])
            course.students.remove(request.user)
            return HttpResponse("Un-subscribed course")
        else:
            return HttpResponseForbidden("Fail to un-subscribe course")
    else:
        return HttpResponseForbidden("Invalid request method, should be POST")
