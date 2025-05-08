from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from users.models import Role, AcademicTitle, StudentProfile, SupervisorProfile
from common.models import Department, Tag

User = get_user_model()

class UserListEndpointTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.department_it = Department.objects.create(name="Wydział IT")
        self.department_el = Department.objects.create(name="Wydział EL")

        self.tag_python = Tag.objects.create(name="Python")
        self.tag_django = Tag.objects.create(name="Django")

        self.student_password = 'student_password'
        self.user_student = User.objects.create_user(
            username='student_test', password=self.student_password, email='s.test@example.com',
            first_name='Student', last_name='Testowy', role=Role.STUDENT,
            description='Initial student description', department=self.department_it
        )
        self.student_profile = StudentProfile.objects.create(user=self.user_student, index_number='S12345')
        self.user_student.tags.add(self.tag_python)

        self.supervisor_password = 'supervisor_password'
        self.user_supervisor_it = User.objects.create_user(
            username='supervisor_it', password=self.supervisor_password, email='p.it@example.com',
            first_name='Promotor', last_name='IT', role=Role.SUPERVISOR,
            academic_title=AcademicTitle.DOCTOR, description='Initial supervisor IT description',
            department=self.department_it
        )
        self.supervisor_profile_it = SupervisorProfile.objects.create(user=self.user_supervisor_it, bacherol_limit=1, engineering_limit=1, master_limit=1, phd_limit=1)
        self.user_supervisor_it.tags.add(self.tag_python, self.tag_django)


        self.supervisor_password_el = 'supervisor_password_el'
        self.user_supervisor_el = User.objects.create_user(
            username='supervisor_el', password=self.supervisor_password_el, email='p.el@example.com',
            first_name='Promotor', last_name='EL', role=Role.SUPERVISOR,
            academic_title=AcademicTitle.PROFESSOR, description='Initial supervisor EL description',
            department=self.department_el
        )
        self.supervisor_profile_el = SupervisorProfile.objects.create(user=self.user_supervisor_el, bacherol_limit=2, engineering_limit=2, master_limit=2, phd_limit=2)


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

        self.user_list_url = reverse('user-list')


    def test_get_user_list_unauthenticated(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_list_authenticated_student(self):
        self.client.force_authenticate(user=self.user_student)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)

        emails = {user_data['email'] for user_data in response.data}
        self.assertIn(self.user_student.email, emails)
        self.assertIn(self.user_supervisor_it.email, emails)
        self.assertIn(self.user_supervisor_el.email, emails)

        for user_data in response.data:
            self.assertIn('url', user_data)
            self.assertIn('email', user_data)
            self.assertIn('role', user_data)
            self.assertNotIn('username', user_data)
            self.assertNotIn('description', user_data)


    def test_get_user_list_authenticated_supervisor(self):
        self.client.force_authenticate(user=self.user_supervisor_it)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)

        emails = {user_data['email'] for user_data in response.data}
        self.assertIn(self.user_student.email, emails)
        self.assertIn(self.user_supervisor_it.email, emails)
        self.assertIn(self.user_supervisor_el.email, emails)


    def test_get_user_list_authenticated_coordinator(self):
        self.client.force_authenticate(user=self.user_coordinator)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)

        emails = {user_data['email'] for user_data in response.data}
        self.assertIn(self.user_student.email, emails)
        self.assertIn(self.user_supervisor_it.email, emails)
        self.assertIn(self.user_supervisor_el.email, emails)
        self.assertNotIn(self.user_coordinator.username, emails)


    def test_get_user_list_authenticated_admin(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)

        emails = {user_data['email'] for user_data in response.data}
        self.assertIn(self.user_student.email, emails)
        self.assertIn(self.user_supervisor_it.email, emails)
        self.assertIn(self.user_supervisor_el.email, emails)


    def test_get_user_detail_unauthenticated(self):
        url = reverse('user-detail', kwargs={'pk': self.user_student.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_student_detail_authenticated(self):
        self.client.force_authenticate(user=self.user_student)
        url = reverse('user-detail', kwargs={'pk': self.user_student.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['username'], self.user_student.username)
        self.assertEqual(response.data['role'], Role.STUDENT)
        self.assertIn('description', response.data)
        self.assertListEqual(sorted(response.data['tags']), sorted([tag.name for tag in self.user_student.tags.all()]))

    def test_get_supervisor_detail_authenticated(self):
        self.client.force_authenticate(user=self.user_student)
        url = reverse('user-detail', kwargs={'pk': self.user_supervisor_it.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['username'], self.user_supervisor_it.username)
        self.assertEqual(response.data['role'], Role.SUPERVISOR)
        self.assertIn('academic_title', response.data)
        self.assertEqual(response.data['academic_title'], AcademicTitle.DOCTOR)
        self.assertListEqual(sorted(response.data['tags']), sorted([tag.name for tag in self.user_supervisor_it.tags.all()]))

    def test_get_user_detail_not_student_or_supervisor(self):
        self.client.force_authenticate(user=self.user_student)
        url = reverse('user-detail', kwargs={'pk': self.user_coordinator.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_detail_nonexistent(self):
        self.client.force_authenticate(user=self.user_student)
        url = reverse('user-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)