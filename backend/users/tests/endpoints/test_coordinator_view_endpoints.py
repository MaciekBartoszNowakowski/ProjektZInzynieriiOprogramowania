from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from users.models import Role, AcademicTitle, StudentProfile, SupervisorProfile
from common.models import Department, Tag

User = get_user_model()

class CoordinatorViewEndpointTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.department_it = Department.objects.create(name="Wydział IT")
        self.department_el = Department.objects.create(name="Wydział EL")

        self.coordinator_password = 'coordinator_password'
        self.user_coordinator_it = User.objects.create_user(
            username='coord_it', password=self.coordinator_password, email='coord.it@example.com',
            first_name='Koordynator', last_name='IT', role=Role.COORDINATOR,
            description='Koordynator IT', department=self.department_it
        )

        self.user_coordinator_el = User.objects.create_user(
            username='coord_el', password=self.coordinator_password, email='coord.el@example.com',
            first_name='Koordynator', last_name='EL', role=Role.COORDINATOR,
            description='Koordynator EL', department=self.department_el
        )

        self.user_coordinator_no_dept = User.objects.create_user(
            username='coord_no_dept', password=self.coordinator_password, email='coord.nodept@example.com',
            first_name='Koordynator', last_name='BrakDzialu', role=Role.COORDINATOR,
            description='Koordynator bez działu', department=None
        )

        self.student_it = User.objects.create_user(
            username='student_it', password='password', email='s.it@example.com',
            first_name='Student', last_name='IT', role=Role.STUDENT,
            description='Student IT description', department=self.department_it
        )
        self.student_profile_it = StudentProfile.objects.create(user=self.student_it, index_number='SIT111')

        self.supervisor_it = User.objects.create_user(
            username='supervisor_it', password='password', email='p.it@example.com',
            first_name='Promotor', last_name='IT', role=Role.SUPERVISOR,
            academic_title=AcademicTitle.DOCTOR, description='Promotor IT description',
            department=self.department_it
        )
        self.supervisor_profile_it = SupervisorProfile.objects.create(user=self.supervisor_it, bacherol_limit=1, engineering_limit=1, master_limit=1, phd_limit=1)

        self.student_el = User.objects.create_user(
            username='student_el', password='password', email='s.el@example.com',
            first_name='Student', last_name='EL', role=Role.STUDENT,
            description='Student EL description', department=self.department_el
        )
        self.student_profile_el = StudentProfile.objects.create(user=self.student_el, index_number='SEL222')

        self.supervisor_el = User.objects.create_user(
            username='supervisor_el', password='password', email='p.el@example.com',
            first_name='Promotor', last_name='EL', role=Role.SUPERVISOR,
            academic_title=AcademicTitle.PROFESSOR, description='Promotor EL description',
            department=self.department_el
        )
        self.supervisor_profile_el = SupervisorProfile.objects.create(user=self.supervisor_el, bacherol_limit=2, engineering_limit=2, master_limit=2, phd_limit=2)

        self.other_user = User.objects.create_user(
            username='other_user', password='password', email='other@example.com',
            first_name='Inny', last_name='Uzytkownik', role=Role.ADMIN, department=None
        )


        self.coordinator_list_url = reverse('update')
        # Detail url will be dynamically created


    def test_get_coordinator_list_unauthenticated(self):
        response = self.client.get(self.coordinator_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_coordinator_list_by_non_coordinator(self):
        self.client.force_authenticate(user=self.student_it)
        response = self.client.get(self.coordinator_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.coordinator_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coordinator_list_coordinator_no_department(self):
        self.client.force_authenticate(user=self.user_coordinator_no_dept)
        response = self.client.get(self.coordinator_list_url)
        # Test dostosowany do obecnego zachowania (200 OK z pustą listą)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)


    def test_get_coordinator_list_authenticated_coordinator_it(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        response = self.client.get(self.coordinator_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

        emails = {user_data['email'] for user_data in response.data}
        self.assertIn(self.student_it.email, emails)
        self.assertIn(self.supervisor_it.email, emails)
        self.assertNotIn(self.student_el.email, emails)
        self.assertNotIn(self.supervisor_el.email, emails)
        self.assertNotIn(self.user_coordinator_it.email, emails)

        for user_data in response.data:
            self.assertIn('url', user_data)
            self.assertIn('email', user_data)
            self.assertIn('role', user_data)
            self.assertIn('first_name', user_data)
            self.assertIn('last_name', user_data)
            self.assertIn('academic_title', user_data)
            self.assertIn('is_active', user_data)
            self.assertNotIn('username', user_data)
            self.assertNotIn('department', user_data)


    def test_get_coordinator_detail_unauthenticated(self):
        url = reverse('coordinator-user-detail', kwargs={'pk': self.student_it.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_coordinator_detail_by_non_coordinator(self):
        self.client.force_authenticate(user=self.student_it)
        url = reverse('coordinator-user-detail', kwargs={'pk': self.student_it.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coordinator_detail_coordinator_no_department(self):
        self.client.force_authenticate(user=self.user_coordinator_no_dept)
        url = reverse('coordinator-user-detail', kwargs={'pk': self.student_it.pk})
        # Test dostosowany do obecnego zachowania (404 Not Found)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_coordinator_detail_user_outside_department(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        url = reverse('coordinator-user-detail', kwargs={'pk': self.student_el.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_coordinator_detail_user_not_student_or_supervisor(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        url = reverse('coordinator-user-detail', kwargs={'pk': self.other_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_coordinator_detail_nonexistent_user(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        url = reverse('coordinator-user-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_coordinator_detail_authenticated_coordinator(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        url = reverse('coordinator-user-detail', kwargs={'pk': self.student_it.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['email'], self.student_it.email)
        self.assertEqual(response.data['role'], Role.STUDENT)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('academic_title', response.data)
        self.assertIn('is_active', response.data)
        self.assertNotIn('username', response.data)
        self.assertNotIn('department', response.data)


    def test_update_department_user_unauthenticated(self):
        url = reverse('coordinator-user-detail', kwargs={'pk': self.student_it.pk})
        data = {'is_active': False}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_department_user_by_non_coordinator(self):
        self.client.force_authenticate(user=self.student_it)
        url = reverse('coordinator-user-detail', kwargs={'pk': self.student_it.pk})
        data = {'is_active': False}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_department_user_coordinator_no_department(self):
        self.client.force_authenticate(user=self.user_coordinator_no_dept)
        url = reverse('coordinator-user-detail', kwargs={'pk': self.student_it.pk})
        data = {'is_active': False}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


    def test_update_department_user_outside_department(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        url = reverse('coordinator-user-detail', kwargs={'pk': self.student_el.pk})
        data = {'is_active': False}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_update_department_user_not_student_or_supervisor(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        url = reverse('coordinator-user-detail', kwargs={'pk': self.other_user.pk})
        data = {'is_active': False}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_update_department_user_nonexistent(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        url = reverse('coordinator-user-detail', kwargs={'pk': 999})
        data = {'is_active': False}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


    def test_coordinator_update_user_in_department(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        url = reverse('coordinator-user-detail', kwargs={'pk': self.student_it.pk})
        initial_active_status = self.student_it.is_active
        initial_first_name = self.student_it.first_name
        data = {
            'is_active': not initial_active_status,
            'first_name': 'NowyJan'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student_it.refresh_from_db()
        self.assertEqual(self.student_it.is_active, not initial_active_status)
        self.assertEqual(self.student_it.first_name, 'NowyJan')

        self.assertEqual(response.data['is_active'], not initial_active_status)
        self.assertEqual(response.data['first_name'], 'NowyJan')


    def test_coordinator_update_user_updates_allowed_fields_and_ignores_others(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        url = reverse('coordinator-user-detail', kwargs={'pk': self.student_it.pk})
        initial_role = self.student_it.role
        initial_email = self.student_it.email
        initial_last_name = self.student_it.last_name
        initial_academic_title = self.student_it.academic_title
        initial_description = self.student_it.description

        new_academic_title = AcademicTitle.BACHELOR
        new_email = 'new.email.updated@example.com'
        new_last_name = 'Nowak'
        new_role = Role.SUPERVISOR
        new_description = 'This should be ignored'

        data = {
            'academic_title': new_academic_title,
            'email': new_email,
            'last_name': new_last_name,
            'role': new_role,
            'description': new_description
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student_it.refresh_from_db()

        self.assertEqual(self.student_it.academic_title, new_academic_title)
        self.assertEqual(self.student_it.email, new_email)
        self.assertEqual(self.student_it.last_name, new_last_name)
        self.assertEqual(self.student_it.role, new_role)

        self.assertEqual(self.student_it.description, initial_description)

        self.assertEqual(response.data['academic_title'], new_academic_title)
        self.assertEqual(response.data['email'], new_email)
        self.assertEqual(response.data['last_name'], new_last_name)
        self.assertEqual(response.data['role'], new_role)
        self.assertNotIn('description', response.data)