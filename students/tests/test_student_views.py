from datetime import datetime

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from students.models import Student, Group

class TestStudentList(TestCase):

    def setUp(self):
        # create groups
        group1, created = Group.objects.get_or_create(
        title="MtM-1")
        group2, created = Group.objects.get_or_create(
        title="MtM-2")
        # create 4 students: 1 for group1 and 3 for group2
        Student.objects.get_or_create(
            first_name="Kid",
            last_name="Napping",
            birthday=datetime.today(),
            ticket='12345',
            student_group=group1)
        Student.objects.get_or_create(
            first_name="Joshua",
            last_name="Friday",
            birthday=datetime.today(),
            ticket='23456',
            student_group=group2)
        Student.objects.get_or_create(
            first_name="Samuel",
            last_name="Jackson",
            birthday=datetime.today(),
            ticket='34567',
            student_group=group2)
        Student.objects.get_or_create(
            first_name="John",
            last_name="Smith",
            birthday=datetime.today(),
            ticket='45678',
            student_group=group2)
        # remember test browser
        self.client = Client()
        # remember url to our homepage
        self.url = reverse('home')

    def test_students_list(self):
        # make request to the server to get homepage page
        response = self.client.get(self.url)
        # have we received OK status from the server?
        self.assertEqual(response.status_code, 200)
        # do we have student name on a page?
        self.assertIn('Kid', response.content)
        # do we have link to student edit form?
        self.assertIn(reverse('students_edit',
            kwargs={'pk': Student.objects.all()[0].id}),
            response.content)
        # ensure we got 3 students, pagination limit is 3
        self.assertEqual(len(response.context['students']), 3)

    def test_current_group(self):
        # set group1 as currently selected group
        group = Group.objects.filter(title="MtM-1")[0]
        self.client.cookies['current_group'] = group.id
        # make request to the server to get homepage page
        response = self.client.get(self.url)
        # in group1 we have only 1 student
        self.assertEqual(len(response.context['students']), 1)


    def test_order_by(self):
        # set order by Last Name
        response = self.client.get(self.url, {'order_by': 'last_name'})
        # now check if we got proper order
        students = response.context['students']
        self.assertEqual(students[0].last_name, 'Friday')
        self.assertEqual(students[1].last_name, 'Jackson')
        self.assertEqual(students[2].last_name, 'Napping')