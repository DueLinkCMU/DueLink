from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
@login_required
def home(request):
    # Display the global posts of all users
    if request.method == 'GET':
        context = {}
        response = render(request, 'duelink/home.html', context)
        return response

