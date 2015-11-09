__author__ = 'pimengfu'
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from models import *
@ensure_csrf_cookie
@login_required
def get_schedule(request):
    # Display the global posts of all users
    if request.method == 'GET':
        user = request.user
        events = user.events.all()
        context = {"events":events}
        response = render(request, 'DueLink/schedule.json', context, content_type='application/json')
        return response
