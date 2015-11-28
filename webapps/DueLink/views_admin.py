from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden, \
    Http404
from forms import *
from models import *


@login_required
@permission_required('DueLink.add_course')
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
            return HttpResponse(form.errors)

@login_required
@permission_required('DueLink.delete_course')
def delete_course(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        context = {'courses': courses}
        return render(request, 'duelink_admin/delete_course.html', context)

    if 'delete_course_name' in request.POST:
        course_name = request.POST['delete_course_name']
        course_number = request.POST['delete_course_number']

        course_to_delete = Course.objects.filter(course_name__exact=course_name)\
            .filter(course_number__exact=course_number)
        course_to_delete.delete()

        return HttpResponse("Delete course %s %s", course_name, course_number)




