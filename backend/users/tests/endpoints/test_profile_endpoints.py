from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from users.models import Role, AcademicTitle, StudentProfile, SupervisorProfile
from common.models import Department, Tag

User = get_user_model()

class ProfileEndpointTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.department_it = Department.objects.create(name="Wydział IT")
        self.tag_python = Tag.objects.create(name="Python")
        self.tag_django = Tag.objects.create(name="Django")

        self.student_password = 'student_password'
        self.user_student = User.objects.create_user(
            username='student_test', password=self.student_password, email='s.test@example.com',
            first_name='Student', last_name='Testowy', role=Role.STUDENT,
            description='Initial student description', department=self.department_it
        )
        self.student_profile = StudentProfile.objects.create(
            user=self.user_student, index_number='S12345'
        )
        self.user_student.tags.add(self.tag_python)

        self.supervisor_password = 'supervisor_password'
        self.user_supervisor = User.objects.create_user(
            username='supervisor_test', password=self.supervisor_password, email='p.test@example.com',
            first_name='Promotor', last_name='Testowy', role=Role.SUPERVISOR,
            academic_title=AcademicTitle.DOCTOR, description='Initial supervisor description',
            department=self.department_it
        )
        self.supervisor_profile = SupervisorProfile.objects.create(
            user=self.user_supervisor, bacherol_limit=2, engineering_limit=3, master_limit=4, phd_limit=1
        )
        self.user_supervisor.tags.add(self.tag_python, self.tag_django)

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

        self.profile_url = reverse('my-profile')

    def test_get_profile_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_student_profile_authenticated(self):
        self.client.force_authenticate(user=self.user_student)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('user', response.data)
        user_data = response.data['user']
        self.assertEqual(user_data['username'], 'student_test')
        self.assertEqual(user_data['role'], Role.STUDENT)
        self.assertIn('index_number', response.data)
        self.assertEqual(response.data['index_number'], 'S12345')
        self.assertListEqual(sorted(user_data['tags']), sorted([self.tag_python.name]))

    def test_get_supervisor_profile_authenticated(self):
        self.client.force_authenticate(user=self.user_supervisor)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('user', response.data)
        user_data = response.data['user']
        self.assertEqual(user_data['username'], 'supervisor_test')
        self.assertEqual(user_data['role'], Role.SUPERVISOR)
        self.assertIn('master_limit', response.data)
        self.assertEqual(response.data['master_limit'], 4)
        self.assertListEqual(sorted(user_data['tags']), sorted([self.tag_python.name, self.tag_django.name]))

    def test_get_coordinator_profile_authenticated(self):
        self.client.force_authenticate(user=self.user_coordinator)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'coordinator_test')
        self.assertEqual(response.data['role'], Role.COORDINATOR)
        self.assertNotIn('index_number', response.data)
        self.assertNotIn('master_limit', response.data)

    def test_get_admin_profile_authenticated(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'admin_test')
        self.assertEqual(response.data['role'], Role.ADMIN)
        self.assertNotIn('index_number', response.data)
        self.assertNotIn('master_limit', response.data)

    def test_update_student_profile_description(self):
        self.client.force_authenticate(user=self.user_student)
        new_description = 'Updated student description via API'
        data = {'user': {'description': new_description}}

        response = self.client.patch(self.profile_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_student.refresh_from_db()
        self.assertEqual(self.user_student.description, new_description)
        self.assertEqual(response.data['user']['description'], new_description)

    def test_update_student_profile_ignores_other_fields(self):
        self.client.force_authenticate(user=self.user_student)
        initial_username = self.user_student.username
        initial_role = self.user_student.role
        initial_first_name = self.user_student.first_name
        initial_index = self.student_profile.index_number
        data = {
            'user': {
                'username': 'new_student_username',
                'role': Role.SUPERVISOR,
                'first_name': 'New Name',
            },
            'index_number': 'S99999'
        }

        response = self.client.patch(self.profile_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_student.refresh_from_db()
        self.student_profile.refresh_from_db()

        self.assertEqual(self.user_student.username, initial_username)
        self.assertEqual(self.user_student.role, initial_role)
        self.assertEqual(self.user_student.first_name, initial_first_name)
        self.assertEqual(self.student_profile.index_number, initial_index)

    def test_update_supervisor_profile_description_and_limits(self):
        self.client.force_authenticate(user=self.user_supervisor)
        new_description = 'Updated supervisor description via API'
        new_master_limit = 99
        data = {
            'user': {'description': new_description},
            'master_limit': new_master_limit
        }

        response = self.client.patch(self.profile_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_supervisor.refresh_from_db()
        self.supervisor_profile.refresh_from_db()

        self.assertEqual(self.user_supervisor.description, new_description)
        self.assertEqual(self.supervisor_profile.master_limit, new_master_limit)

        self.assertEqual(response.data['user']['description'], new_description)
        self.assertEqual(response.data['master_limit'], new_master_limit)

    def test_update_supervisor_profile_ignores_other_fields(self):
        self.client.force_authenticate(user=self.user_supervisor)
        initial_academic_title = self.user_supervisor.academic_title
        initial_last_name = self.user_supervisor.last_name
        initial_bachelor_limit = self.supervisor_profile.bacherol_limit
        initial_engineering_limit = self.supervisor_profile.engineering_limit

        invalid_data = {
            'engineering_limit': 'invalid_limit'
        }

        response = self.client.patch(self.profile_url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_update_coordinator_profile_description(self):
        self.client.force_authenticate(user=self.user_coordinator)
        new_description = 'Updated coordinator description via API'
        data = {'description': new_description}

        response = self.client.patch(self.profile_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_coordinator.refresh_from_db()
        self.assertEqual(self.user_coordinator.description, new_description)
        self.assertEqual(response.data['description'], new_description)

    def test_update_coordinator_profile_ignores_other_fields(self):
        self.client.force_authenticate(user=self.user_coordinator)
        initial_username = self.user_coordinator.username
        initial_email = self.user_coordinator.email
        initial_role = self.user_coordinator.role
        initial_academic_title = self.user_coordinator.academic_title
        data = {
            'username': 'new_coordinator_username',
            'email': 'new_coord_email@example.com',
            'description': 'This description should be updated',
            'role': Role.ADMIN,
            'academic_title': AcademicTitle.PROFESSOR
        }

        response = self.client.patch(self.profile_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_coordinator.refresh_from_db()

        self.assertEqual(self.user_coordinator.username, initial_username)
        self.assertEqual(self.user_coordinator.email, initial_email)
        self.assertEqual(self.user_coordinator.description, 'This description should be updated')
        self.assertEqual(self.user_coordinator.role, initial_role)
        self.assertEqual(self.user_coordinator.academic_title, initial_academic_title)

    def test_update_admin_profile_description(self):
        self.client.force_authenticate(user=self.user_admin)
        new_description = 'Updated admin description via API'
        data = {'description': new_description}

        response = self.client.patch(self.profile_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_admin.refresh_from_db()
        self.assertEqual(self.user_admin.description, new_description)
        self.assertEqual(response.data['description'], new_description)

    def test_update_admin_profile_ignores_other_fields(self):
        self.client.force_authenticate(user=self.user_admin)
        initial_first_name = self.user_admin.first_name
        initial_last_name = self.user_admin.last_name
        initial_email = self.user_admin.email
        data = {
            'first_name': 'New Admin First',
            'last_name': 'New Admin Last',
            'description': 'Admin description update test',
            'email': 'new_admin_email_2@example.com',
        }

        response = self.client.patch(self.profile_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_admin.refresh_from_db()

        self.assertEqual(self.user_admin.first_name, initial_first_name)
        self.assertEqual(self.user_admin.last_name, initial_last_name)
        self.assertEqual(self.user_admin.description, 'Admin description update test')
        self.assertEqual(self.user_admin.email, initial_email)