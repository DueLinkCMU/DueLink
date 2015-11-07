SchoolForm:
```python
from DueLink.models import *
from DueLink.forms import *
arr = {'name': 'central michigan univ'}
form = SchoolForm(arr)
valid_test = form.is_valid
print(valid_test)
form.save()

School.objects.all()
```

ProfileForm:
```python
from DueLink.models import *
from DueLink.forms import *

cmu = School.objects.get(name='central michigan univ')
test_user = User.objects.get(username='test_user')
info = {'nick_name': 'xgy', 'school': cmu.pk,}

new_profile = Profile(user=test_user)
form = ProfileForm(info, instance=new_profile)
form.is_valid()
#should return True

form.save()
```