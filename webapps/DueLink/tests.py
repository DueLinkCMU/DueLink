from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from DueLink.models import *


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


class DueLinkCourseMgmtTest(TestCase):
    fixtures = ['test_data.json']
    def test_add_course(self):
        client = Client()
        client.login(username='admin2', password='123')
        post_context = {'course_name': 'unittest', 'course_number': '15315',
                                  'section': 'A', 'instructor': 'RB', 'school': "1"}

        response = client.post('/duelink/admin/add_course', post_context, follow=True)
        self.assertTrue(Course.objects.filter(course_name='unittest').count() == 1)
        self.assertTrue(response.content.find('Successfully'.encode()) >= 0)

        # The app should not add new course as it has duplicated section
        response_duplicate_request = client.post('/duelink/admin/add_course'
                                                 , post_context, follow=True)
        self.assertEqual(Course.objects.filter(course_name='unittest').count(), 1)

        # Test adding new section, should be OK
        post_context['section'] = 'N'
        response_new_section = client.post('/duelink/admin/add_course', post_context, follow=True)
        self.assertTrue(response.content.find('Successfully'.encode()) >= 0)
        self.assertEqual(Course.objects.filter(course_name='unittest').count(), 2)


    def test_delete_course(self):
        client = Client()
        client.login(username='admin2', password='123')
        response = client.post('/duelink/admin/delete_course', {'courses': 1})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Course.objects.filter(pk = 1).count() == 0)

        # test no permission client
        client_no_perm = Client()
        response_no_perm = client_no_perm.post('/duelink/admin/delete_course', {'courses': 1})
        self.assertEqual(response_no_perm.status_code, 302)
