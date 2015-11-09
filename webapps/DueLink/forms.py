from datetime import datetime
from django import forms
from models import *
from django.forms.extras.widgets import SelectDateWidget


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nick_name', 'school', 'profile_image')


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ('name',)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('students',)

    def clean_section(self):
        cleaned_data = super(CourseForm, self).clean()
        if Course.objects.filter(course_number=cleaned_data['course_number']).count() > 0:
            courses_same_course_num = Course.objects.filter(course_number=cleaned_data['course_number'])
            for each in courses_same_course_num:
                if each.section == cleaned_data['section']:
                    return False
        else:
            return True


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

class TaskForm(forms.ModelForm):
    finished = forms.TypedChoiceField(coerce=lambda x: bool(int(x)),
                                      choices=((0, 'Unfinished'), (1, 'Finished')),
                                      widget=forms.Select
                                      )

    class Meta:
        model = Task
        fields = ('finished',)


class RegistrationForm(forms.Form):
    # TODO: form attrs
    username = forms.CharField(max_length=30, label='username', widget=forms.TextInput())
    email = forms.EmailField(max_length=100, label='email', widget=forms.EmailInput())
    password1 = forms.CharField(max_length=30, label='password1', widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=30, label='password2', widget=forms.PasswordInput())

    nick_name = forms.CharField(max_length=30, label='nickname', widget=forms.TextInput())
    school = forms.ModelChoiceField(queryset=School.objects.all())

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The two passwords doesn't match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("The username is occupied, please try another one.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("This email is occupied.")

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
    name = forms.CharField(max_length=20, label='name')
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    # due = forms.DateTimeField() # TODO: format

    deadline_date = forms.CharField(max_length=30)
    deadline_time = forms.CharField(max_length=30)

    def clean(self):
        cleaned_data = super(AddEventForm, self).clean()
        return cleaned_data

    def clean_datetime(self):
        date = self.cleaned_data['deadline_date']
        time = self.cleaned_data['deadline_time']
        date_time_str = date + " " + time

        due_datetime = datetime.strptime(date_time_str, "%m/%d/%Y %H:%M")
        # if due_date > datetime.now():
        # TODO: validation

        return due_datetime

        # def clean_course(self):
        #     course_pk = self.cleaned_data['course']
        #     if Course.objects.filter(pk=course_pk).count() == 0:
        #         return 0
        #     else: # course more than 1?
        #         return course_pk
