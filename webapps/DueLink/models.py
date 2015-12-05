from django.db import models
from django.contrib.auth.models import User


# FINISHED_CHOICES = ((False, 'Unfinished'), (True, 'Finished'))


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

    @property
    def get_courses(self):
        return Course.objects.filter(students=self.user)


class Course(models.Model):
    course_number = models.CharField(max_length=10)
    course_name = models.CharField(max_length=80)
    section = models.CharField(max_length=5)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    instructor = models.CharField(max_length=80)
    students = models.ManyToManyField(User, related_name='course_students')

    def __unicode__(self):
        return self.school.name + ": " + self.course_number + " " + self.course_name + "/" + self.section


class Deadline(models.Model):
    name = models.CharField(max_length=20)
    due = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ManyToManyField(User)

    def __unicode__(self):
        return self.course.school.name + ", " + self.course.course_name + ", " \
               + self.name + " due on " + self.due.__str__()


class Team(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="members")

    def __unicode__(self):
        return self.id.__str__() + "," +self.name + ',' + self.users.all().__str__()


class DueEvent(models.Model):
    deadline = models.ForeignKey(Deadline, related_name='events', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='events', on_delete=models.CASCADE, null=True)
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
            return int(round(float(finished) / total * 100))
        else:
            return 0


class Task(models.Model):
    event = models.ForeignKey(DueEvent, related_name='tasks', on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    description = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.event.deadline.name + ", " + str(self.finished) + ", " + self.description + ", " \
               + self.created_time.__str__()

