from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_user')
    nick_name = models.CharField(max_length=20)
    school = models.ForeignKey(School)
    profile_image = models.ImageField(upload_to='user_images', blank=True)
    friends = models.ManyToManyField(User, related_name='profile_friends')

    def __unicode__(self):
        return self.nick_name


class School(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    course_number = models.CharField(max_length=10)
    course_name = models.CharField(max_length=50)
    section = models.CharField(max_length=1)
    school = models.ForeignKey(School)
    instructor = models.CharField(max_length=40)
    students = models.ManyToManyField(User, related_name='course_students')

    def __unicode__(self):
        return self.school + ": " + self.course_name


class Deadline(models.Model):
    name = models.CharField(max_length=20)
    due = models.DateTimeField()
    course = models.ForeignKey(Course)
    students = models.ManyToManyField(User)

    def __unicode__(self):
        return self.course.school + ", " + self.course.course_name + ", "\
               + self.name + " due on " + self.due


class Task(models.Model):
    deadline = models.ForeignKey(Deadline)
    status = models.BooleanField()
    description = models.CharField(max_length=100)
    timestamp = models.DateTimeField()

