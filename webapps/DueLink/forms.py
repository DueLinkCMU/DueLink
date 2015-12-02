from datetime import datetime
import dateutil.parser
from django import forms
from forms import *
from DueLink.models import *
import views
from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden, \
    Http404
from django.forms.extras.widgets import SelectDateWidget


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nick_name', 'school', 'profile_image')


class AddSchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ('name',)


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('students',)

    def clean_section(self):
        cleaned_data = super(AddCourseForm, self).clean()
        # Check both courses with same name and num
        courses_same_course_num = Course.objects.filter(course_number=cleaned_data['course_number'])
        courses_same_course_name = Course.objects.filter(course_number=cleaned_data['course_name'])
        courses_exist = courses_same_course_num | courses_same_course_name
        if courses_exist.count() > 0:
            for each in courses_exist:
                if each.section == cleaned_data['section']:
                    raise forms.ValidationError("Section invalid")
            # if no return, any request with existing course num will be fail
            return cleaned_data['section']
        else:
            return cleaned_data['section']


class AddSectionForm(forms.Form):
    origin_course = forms.ModelChoiceField(queryset=Course.objects.all())
    new_section = forms.CharField(max_length=4)
    new_instructor = forms.CharField(max_length=80, required=False, label='Instructor, blank if the same')

    def clean(self):
        cleaned_data = super(AddSectionForm, self).clean()
        return cleaned_data

    def clean_new_section(self):
        course = self.cleaned_data['origin_course']
        courses_same_course_num = Course.objects.filter(course_number=course.course_number)
        courses_same_course_name = Course.objects.filter(course_number=course.course_name)
        courses_exist = courses_same_course_num | courses_same_course_name

        if courses_exist.count() > 0:
            for each in courses_exist:
                if each.section == self.cleaned_data['new_section']:
                    raise forms.ValidationError("Section invalid")
            # if no return, any request with existing course num will be fail
            return self.cleaned_data['new_section']
        else:
            return self.cleaned_data['new_section']


class DeleteCourseForm(forms.Form):
    courses = forms.ModelChoiceField(queryset=Course.objects.all())

    def clean(self):
        cleaned_data = super(DeleteCourseForm, self).clean()
        return cleaned_data


class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Deadline
        exclude = ('students',)
        widgets = {'due': SelectDateWidget}


# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ('finished',)
#         widgets = {'finished': forms.Select}
#

class UpdateTaskForm(forms.ModelForm):
    finished = forms.TypedChoiceField(coerce=lambda x: bool(int(x)),
                                      choices=((0, 'Unfinished'), (1, 'Finished')),
                                      widget=forms.Select()
                                      )

    class Meta:
        model = Task
        fields = ('finished',)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('description',)


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, label='Username', widget=forms.TextInput())
    email = forms.EmailField(max_length=100, label='Email', widget=forms.EmailInput())
    password1 = forms.CharField(max_length=30, label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=30, label='Confirm Password', widget=forms.PasswordInput())
    nick_name = forms.CharField(max_length=30, label='Nickname', widget=forms.TextInput())
    school = forms.ModelChoiceField(queryset=School.objects.all())

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(("The two passwords doesn't match."))
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError(("The username is occupied, please try another one."))

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError(("This email is occupied."))

        return email

        # TODO: clean school


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class EditProfileForm(ProfileForm):
    class Meta(ProfileForm.Meta):
        model = Profile
        fields = ProfileForm.Meta.fields + ('profile_image',)


class AddEventForm(forms.Form):
    name = forms.CharField(max_length=20, label='Event Name')
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    deadline_datetime = forms.CharField(widget=forms.DateTimeInput(attrs={'type': 'hidden'}))

    # TODO: validate add only course you select
    def clean(self):
        cleaned_data = super(AddEventForm, self).clean()
        return cleaned_data

    def clean_deadline_datetime(self):
        datetime_str = self.cleaned_data['deadline_datetime']

        try:
            due_datetime = dateutil.parser.parse(datetime_str)
        except ValueError:
            print("ValueError of dateutil.parser")
            raise forms.ValidationError(('DateUtil parse error'))
        except Exception as e:
            print("Exception" + str(e))
            raise forms.ValidationError(("Datetime unexpected errors"))

        return due_datetime

    def clean_deadline(self, request):
        print("run clean_deadline")
        name = self.cleaned_data['name']
        due_datetime = self.cleaned_data['deadline_datetime']
        course_pk = self.cleaned_data['course']
        deadline_set = Deadline.objects.filter(course=course_pk, due=due_datetime)

        # # Check if the deadline exists.
        if deadline_set:
            # If the deadline exists, and the event exists
            if DueEvent.objects.filter(deadline=deadline_set[0], user=request.user):
                return False
            deadline = deadline_set[0]
        else:
            # Call add_deadline in views.py
            deadline = views.add_deadline(request, name, due_datetime, course_pk)

        return deadline


class SubscribeCourseForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())

    def clean(self):
        cleaned_data = super(SubscribeCourseForm, self).clean()
        return cleaned_data

    def clean_exist(self, user):
        course = self.cleaned_data['course']
        print(course)
        print(user)
        try:
            if user in course.students.all():
                return False
            return True
        except Http404:
            print("Course not exist")
            return False
        except Exception:
            print("Unexpected error: course is not Course object or user is not User object")
            return False
