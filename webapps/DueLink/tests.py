from django.test import TestCase, Client, TransactionTestCase, SimpleTestCase
from DueLink.models import School, DueEvent, Course, Task
import DueLink

class DueLinkModelsTest(TestCase):
    def test_simple_add(self):
        self.assertTrue(School.objects.all().count() == 0)
        new_school = School(name='A test school')
        new_school.save()
        self.assertTrue(School.objects.all().count() == 1)
        self.assertTrue(School.objects.filter(name__contains='test'))


class DueLinkTest(TestCase):
    def test_login_page(self):  # Tests that a GET request to /sio/
        client = Client()  # results in an HTTP 200 (OK) response.
        response = client.get('/duelink/login')
        self.assertEqual(response.status_code, 200)


class DueLinkTestSchool(TestCase):
    fixtures = ['test_data.json']

    def test_add_school(self):
        client2 = Client()
        client2.login(username='admin2', password='123')
        response = client2.post('/duelink/admin/add_school', {'name': "testbbbb"}, follow=True)
        self.assertTrue(School.objects.filter(name='testbbbb').count() > 0)


class DueLinkEventTest(TestCase):
    fixtures = ['test_data.json']

    def test_adding_event(self):
        client = Client()
        client.login(username='admin2', password='123')

        context = {'name': 'test', 'course': 2, 'deadline_datetime': '2015-11-29T12:34:00+00:00'}
        response = client.post('/duelink/add_event', context)
        self.assertEqual(DueEvent.objects.filter(deadline__name='test').count(), 1)


class DueLinkGetTaskTest(TestCase):
    fixtures = ['test_data.json']

    def test_get_tast(self):
        client = Client()
        client.login(username='admin2', password='123')
        response = client.get('/duelink/get_tasks/1')
        self.assertEqual(response.status_code, 200)

class DueLinkTaskTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin2', password='123')

    def test_add_task(self):
        response = self.client.post('/duelink/add_task', {'event_id': '1', 'description': 'Test_task'})
        self.assertTrue(response.content.find('Test_task'.encode()) > 0)

        # Test none-exist event id, should return 404
        response_nonexist_event = self.client.post('/duelink/add_task',
                                                   {'event_id': '10086', 'description': 'Test_task_nonexist'})
        self.assertEqual(response_nonexist_event.status_code, 404)

    def test_change_task_status(self):
        old_status = Task.objects.get(pk=1).finished
        response = self.client.post('/duelink/update_task/' + '1')
        self.assertNotEqual(Task.objects.get(pk=1).finished, old_status)

class DueLinkTestForm(TestCase):
    fixtures = ['test_data.json']
    def test_form(self):
        course = Course.objects.get(pk=1)
        form = DueLink.forms.AddEventForm({'origin_course': course, 'new_section': course.section})
        form.is_valid()
        self.assertFalse(form.is_valid())


class DueLinkAddCourseTest(TransactionTestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin3', password='123')

    def test_add_course(self):
        post_context = {'course_name': 'unittest', 'course_number': '15315',
                        'section': 'A', 'instructor': 'RB', 'school': "1"}
        response = self.client.post('/duelink/admin/add_course', post_context, follow=True)
        self.assertTrue(Course.objects.filter(course_name='unittest').count() == 1)
        self.assertTrue(response.content.find('Successfully'.encode()) > 0)

        # The app should not add new course as it has duplicated section
        self.client.post('/duelink/admin/add_course'
                         , post_context, follow=True)
        self.assertEqual(Course.objects.filter(course_name='unittest').count(), 1)

        # Test adding new section, should be OK
        post_context['section'] = 'N'
        response_new_section = self.client.post('/duelink/admin/add_course', post_context, follow=True)
        self.assertTrue(response_new_section.content.find('Successfully'.encode()) > 0)
        self.assertEqual(Course.objects.filter(course_name='unittest').count(), 2)


class DueLinkDeleteCourseTest(TransactionTestCase):
    def test_delete_course(self):
        client = Client()
        client.login(username='admin2', password='123')
        response = self.client.post('/duelink/admin/delete_course', {'courses': 1}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Course.objects.filter(id=1).count() == 0)

        # test no permission client, should be redirect to login
        client_no_perm = Client()
        response_no_perm = client_no_perm.post('/duelink/admin/delete_course', {'courses': 1})
        self.assertEqual(response_no_perm.status_code, 302)

