from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_user')
    nick_name = models.CharField(max_length=20)
    school = models.ForeignKey(School)
    profile_image = models.ImageField(upload_to='user_images', blank=True, default='default_user.jpg')
    friends = models.ManyToManyField(User, related_name='profile_friends')

    def __unicode__(self):
        return self.nick_name


class Course(models.Model):
    course_number = models.CharField(max_length=10)
    course_name = models.CharField(max_length=50)
    section = models.CharField(max_length=4)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    instructor = models.CharField(max_length=40)
    students = models.ManyToManyField(User, related_name='course_students')

    def __unicode__(self):
        return self.school.name + ": " + self.course_name


class Deadline(models.Model):
    name = models.CharField(max_length=20)
    due = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ManyToManyField(User)

    def __unicode__(self):
        return self.course.school.name + ", " + self.course.course_name + ", " \
               + self.name + " due on " + self.due.__str__()


class DueEvent(models.Model):
    deadline = models.ForeignKey(Deadline, related_name='events', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)

    @property
    def progress(self):
        if self.finished:
            return 100
        total = self.tasks.all().count()
        if total:
            finished = 0
            for task in self.tasks.all():
                if task.finished:
                    finished += 1
            return round(float(finished) / total, 2) * 100
        else:
            return 0


class Task(models.Model):
    deadline = models.ForeignKey(DueEvent, related_name='tasks', on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    description = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.deadline + ", " + self.finished.__str__() + ", " + self.description + ", " \
               + self.created_time.__str__()
