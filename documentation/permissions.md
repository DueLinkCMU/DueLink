https://docs.djangoproject.com/en/1.8/topics/auth/default/  

from django.contrib.auth.models import Group, Permission   

Group.objects.create(name="duelink_admin")  

g.permissions.all()
m django.contrib.auth.models import Permission


Permission.objects.all()

t = Permission.objects.get(codename__icontains='add_course')
g = Group.objects.get(name="duelink_admin")

g.permissions.add(t)



