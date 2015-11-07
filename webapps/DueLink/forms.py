from django import forms
from django.forms import ModelForm
from webapps.DueLink.models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nick_name', 'school', 'profile_image']


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['students']


class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Deadline
        exclude = ['students']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['timestamp']
