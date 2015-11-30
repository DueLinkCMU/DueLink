from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden, \
    Http404
from forms import *
from models import *


@permission_required('DueLink.add_course')
@permission_required('DueLink.delete_course')
@login_required
def manage_course(request):
    if not request.method == 'GET':
        return HttpResponseForbidden("Invalid method")

    return HttpResponseRedirect(reverse('add_course'))


@login_required
@permission_required('DueLink.add_course')
def add_course(request):
    if request.method == 'GET':
        form = AddCourseForm()
        context = {'add_course_form': form, 'add_course': True}
        return render(request, 'duelink_admin/add_course.html', context)

    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():  # Validate input data & duplicate course sections
            form.save()
            response_form = AddCourseForm()
            context = {'add_course_form': response_form, 'success_flag': True, 'add_course': True}
            return render(request, 'duelink_admin/add_course.html', context)
        else:
            context = {'add_course_form': form, 'fail_flag': True, 'add_course': True}
            return render(request, 'duelink_admin/add_course.html', context)


@login_required
@permission_required('DueLink.add_course')
def add_section(request):
    if request.method == 'GET':
        form = AddSectionForm()
        context = {'add_section_form': form, 'add_section': True}
        return render(request, 'duelink_admin/add_section.html', context)

    if request.method == 'POST':
        form = AddSectionForm(request.POST)
        if form.is_valid():
            origin_course = form.cleaned_data['origin_course']
            new_course = Course(course_name=origin_course.course_name, course_number=origin_course.course_number,
                                school=origin_course.school)
            new_course.section =  form.cleaned_data['new_section']
            if form.cleaned_data['new_instructor'] == None:
                new_course.instructor = origin_course.instructor
            else:
                new_course.instructor = form.cleaned_data['new_instructor']
            new_course.save()

            response_form = AddSectionForm()
            context = {'add_section_form': response_form, 'success_flag': True, 'add_section': True}
            return render(request, 'duelink_admin/add_section.html', context)
        else:
            context = {'add_section_form': form, 'fail_flag': True, 'add_section': True}
            return render(request, 'duelink_admin/add_section.html', context)







@login_required
@permission_required('DueLink.delete_course')
def delete_course(request):
    if request.method == 'GET':
        form = DeleteCourseForm()
        context = {'delete_course_form': form, 'delete_course': True}
        return render(request, 'duelink_admin/delete_course.html', context)

    if request.method == 'POST':
        form = DeleteCourseForm(request.POST)
        if form.is_valid():
            # TODO: 404
            course = form.cleaned_data['courses']
            course.delete()
            response_form = DeleteCourseForm()
            context = {'delete_course_form': response_form, 'success_flag': True, 'delete_course': True}
            return render(request, 'duelink_admin/delete_course.html', context)
        else:
            context = {'delete_course_form': form, 'fail_flag': True, 'delete_course': True}
            return render(request, 'duelink_admin/delete_course.html', context)

@login_required
@permission_required('DueLink.add_school')
def add_school(request):
    if request.method == 'GET':
        form = AddSchoolForm()
        context = {'add_school_form': form, 'add_school': True}
        return render(request, 'duelink_admin/add_school.html', context)

    if request.method == 'POST':
        form = AddSchoolForm(request.POST)
        if form.is_valid():
            form.save()
            context = {'add_school_form': form, 'add_school': True, 'success_flag': True}
            return render(request, 'duelink_admin/add_school.html', context)
        else:
            context = {'add_school_form': form, 'add_school': True, 'fail_flag': True}
            return render(request, 'duelink_admin/add_school.html', context)


