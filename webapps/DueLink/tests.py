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
    def test_home_page(self):  # Tests that a GET request to /sio/
        client = Client()  # results in an HTTP 200 (OK) response.
        response = client.get('/duelink/')
        self.assertEqual(response.status_code, 200)
