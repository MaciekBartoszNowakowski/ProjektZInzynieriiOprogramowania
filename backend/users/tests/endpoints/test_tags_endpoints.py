from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from users.models import Role, AcademicTitle, StudentProfile, SupervisorProfile
from common.models import Department, Tag

User = get_user_model()

class TagsEndpointTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.department_it = Department.objects.create(name="Wydział IT")

        self.tag_python = Tag.objects.create(name="Python")
        self.tag_django = Tag.objects.create(name="Django")
        self.tag_rest = Tag.objects.create(name="REST API")
        self.tag_db = Tag.objects.create(name="Bazy Danych")

        self.student_password = 'student_password'
        self.user_student = User.objects.create_user(
            username='student_test', password=self.student_password, email='s.test@example.com',
            first_name='Student', last_name='Testowy', role=Role.STUDENT,
            description='Initial student description', department=self.department_it
        )
        self.user_student.tags.add(self.tag_python, self.tag_django)

        self.supervisor_password = 'supervisor_password'
        self.user_supervisor = User.objects.create_user(
            username='supervisor_test', password=self.supervisor_password, email='p.test@example.com',
            first_name='Promotor', last_name='Testowy', role=Role.SUPERVISOR,
            academic_title=AcademicTitle.DOCTOR, description='Initial supervisor description',
            department=self.department_it
        )
        self.user_supervisor.tags.add(self.tag_python, self.tag_django, self.tag_rest)

        self.coordinator_password = 'coordinator_password'
        self.user_coordinator = User.objects.create_user(
            username='coordinator_test', password=self.coordinator_password, email='k.test@example.com',
            first_name='Koordynator', last_name='Testowy', role=Role.COORDINATOR,
            description='Initial coordinator description', department=self.department_it
        )

        self.admin_password = 'admin_password'
        self.user_admin = User.objects.create_superuser(
            username='admin_test', password=self.admin_password, email='a.test@example.com',
            first_name='Admin', last_name='Testowy', role=Role.ADMIN,
            description='Initial admin description', department=self.department_it
        )

        self.tags_url = reverse('update-tags')

    def test_get_tags_unauthenticated(self):
        response = self.client.get(self.tags_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_student_tags_authenticated(self):
        self.client.force_authenticate(user=self.user_student)
        response = self.client.get(self.tags_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_tags = sorted([self.tag_python.name, self.tag_django.name])
        returned_tags = sorted([tag_data['name'] for tag_data in response.data])
        self.assertListEqual(returned_tags, expected_tags)

    def test_get_supervisor_tags_authenticated(self):
        self.client.force_authenticate(user=self.user_supervisor)
        response = self.client.get(self.tags_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_tags = sorted([self.tag_python.name, self.tag_django.name, self.tag_rest.name])
        returned_tags = sorted([tag_data['name'] for tag_data in response.data])
        self.assertListEqual(returned_tags, expected_tags)

    def test_get_coordinator_tags_authenticated(self):
        self.client.force_authenticate(user=self.user_coordinator)
        response = self.client.get(self.tags_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    def test_get_admin_tags_authenticated(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.get(self.tags_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    def test_update_student_tags_authenticated(self):
        self.client.force_authenticate(user=self.user_student)
        data = {
            'to_add': [self.tag_rest.id, self.tag_db.id],
            'to_remove': [self.tag_django.id]
        }
        response = self.client.put(self.tags_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user_student.refresh_from_db()
        expected_tags = sorted([self.tag_python.name, self.tag_rest.name, self.tag_db.name])
        updated_tags = sorted([tag.name for tag in self.user_student.tags.all()])
        self.assertListEqual(updated_tags, expected_tags)

        response_tags = sorted([tag_data['name'] for tag_data in response.data])
        self.assertListEqual(response_tags, expected_tags)


    def test_update_supervisor_tags_authenticated(self):
        self.client.force_authenticate(user=self.user_supervisor)
        data = {
            'to_add': [self.tag_db.id],
            'to_remove': [self.tag_python.id, self.tag_rest.id]
        }
        response = self.client.put(self.tags_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user_supervisor.refresh_from_db()
        expected_tags = sorted([self.tag_django.name, self.tag_db.name])
        updated_tags = sorted([tag.name for tag in self.user_supervisor.tags.all()])
        self.assertListEqual(updated_tags, expected_tags)

        response_tags = sorted([tag_data['name'] for tag_data in response.data])
        self.assertListEqual(response_tags, expected_tags)

    def test_update_tags_with_invalid_tag_id(self):
        self.client.force_authenticate(user=self.user_student)
        data = {
            'to_add': [self.tag_rest.id, 999],
            'to_remove': []
        }
        response = self.client.put(self.tags_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('to_add', response.data)

    def test_update_tags_with_non_list_data(self):
        self.client.force_authenticate(user=self.user_student)
        data = {
            'to_add': self.tag_rest.id,
            'to_remove': []
        }
        response = self.client.put(self.tags_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('to_add', response.data)

    def test_update_tags_unauthenticated(self):
        data = {
            'to_add': [self.tag_rest.id],
            'to_remove': []
        }
        response = self.client.put(self.tags_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)