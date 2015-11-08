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
        print "what the hell?"
        context = {}
        response = render(request, 'DueLink/schedule.json', context)
        return response
