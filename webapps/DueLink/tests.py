from django.test import TestCase, Client, TransactionTestCase, SimpleTestCase
from DueLink.models import School, DueEvent, Course, Task
import DueLink


# http://stackoverflow.com/questions/853796/problems-with-contenttypes-when-loading-a-fixture-in-django

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


class DueLinkTestAddSchool(TestCase):
    fixtures = ['test_data2.json']

    def test_add_school(self):
        client2 = Client()
        client2.login(username='admin2', password='123')
        response = client2.post('/duelink/admin/add_school', {'name': "testbbbb"}, follow=True)
        self.assertTrue(School.objects.filter(name='testbbbb').count() > 0)
        response = client2.post('/duelink/admin/add_school', {'name': "testbbbb"}, follow=True)
        self.assertTrue(response.content.find('Fail'.encode()) > 0)


class DueLinkEventTest(TestCase):
    fixtures = ['test_data2.json']

    def test_adding_event(self):
        client = Client()
        client.login(username='admin2', password='123')
        context = {'name': 'test', 'course': 2, 'deadline_datetime': '2015-11-29T12:34:00+00:00'}
        response = client.post('/duelink/add_event', context)
        self.assertEqual(DueEvent.objects.filter(deadline__name='test').count(), 1)


class DueLinkGetTaskTest(TestCase):
    fixtures = ['test_data2.json']

    def test_get_tast(self):
        client = Client()
        client.login(username='admin2', password='123')
        response = client.get('/duelink/get_tasks/1')
        self.assertEqual(response.status_code, 200)


class DueLinkTaskTest(TestCase):
    fixtures = ['test_data2.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin2', password='123')

    def test_add_task(self):
        response = self.client.post('/duelink/add_task', {'event_id': '1', 'description': 'Test_task'})
        self.assertTrue(response.content.find('Test_task'.encode()) > 0)

        # Test none-exist event id, should return 404
        response_noneexist_event = self.client.post('/duelink/add_task',
                                                   {'event_id': '10086', 'description': 'Test_task_none_exist'})
        self.assertEqual(response_noneexist_event.status_code, 404)

    def test_change_task_status(self):
        old_status = Task.objects.get(pk=1).finished
        response = self.client.post('/duelink/update_task/' + '1')
        self.assertNotEqual(Task.objects.get(pk=1).finished, old_status)


class DueLinkTestForm(TestCase):
    fixtures = ['test_data2.json']

    def test_form(self):
        course = Course.objects.get(pk=1)
        # Test adding existing section, form.is_valid() should be False
        form = DueLink.forms.AddEventForm({'origin_course': course, 'new_section': course.section})
        form.is_valid()
        self.assertFalse(form.is_valid())


class DueLinkAddCourseTest(TransactionTestCase):
    fixtures = ['test_data2.json']

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
    fixtures = ['test_data2.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin2', password='123')

    def test_delete_course(self):
        response = self.client.post('/duelink/admin/delete_course', {'courses': '1'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Course.objects.filter(pk=1).count() == 0)

        # test no permission client, should be redirect to login
        client_no_perm = Client()
        response_no_perm = client_no_perm.post('/duelink/admin/delete_course', {'courses': 1})
        self.assertEqual(response_no_perm.status_code, 302)

    def test_delete_none_exist(self):
        response = self.client.post('/duelink/admin/delete_course', {'course': 10000}, follow=True)
        self.assertTrue(response.content.find('Fail'.encode()) >= 0)


class AddSectionTest(TransactionTestCase):
    fixtures = ['test_data2.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin2', password='123')

    def test_add_section(self):
        course = Course(course_name='unittest', course_number='15315', section='A', instructor='RB', school_id=1)
        course.save()
        post_context = {'origin_course': str(course.pk), 'new_section': 'X', 'new_instructor': 'CD'}
        response = self.client.post('/duelink/admin/add_section', post_context)
        self.assertTrue(Course.objects.filter(course_name='unittest', section='X', instructor='CD').exists())

        # Test add section without input new_instructor
        post_context = {'origin_course': str(course.pk), 'new_section': 'Y'}
        response = self.client.post('/duelink/admin/add_section', post_context)
        self.assertTrue(Course.objects.filter(course_name='unittest', section='Y').exists())

        # Test add duplicated section
        post_context = {'origin_course': str(course.pk), 'new_section': 'A'}
        response = self.client.post('/duelink/admin/add_section', post_context)
        self.assertTrue(response.content.find('Fail'.encode()) > 0)


class AdminAccessTest(TransactionTestCase):
    fixtures = ['test_data2.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin2', password='123')

    def test_admin(self):
        response = self.client.get('/duelink/admin/add_course')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/duelink/admin/delete_course')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/duelink/admin/add_school')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/duelink/admin/add_section')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/duelink/admin/manage_course', follow=True)
        self.assertEqual(response.status_code, 200)

class DueLinkAcessTest(TransactionTestCase):
    fixtures = ['test_data2.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin2', password='123')

    def test_admin(self):
        response = self.client.get('/duelink/home')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/duelink/friend_list')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/duelink/friend_stream')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/duelink/profile/1')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/duelink/profile/10086')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/duelink/profile_image/1')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/duelink/add_event')
        self.assertEqual(response.status_code, 200)

        # TODO:Can any user visit any other users' task?
        # response = self.client.get('/duelink/tasks/1')
        # self.assertEqual(response.status_code, 200)

        response = self.client.get('/duelink/get_tasks/1')
        self.assertEqual(response.status_code, 200)

