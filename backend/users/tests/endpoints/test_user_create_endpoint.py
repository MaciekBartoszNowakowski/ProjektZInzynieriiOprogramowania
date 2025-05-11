from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from users.models import Role, AcademicTitle, StudentProfile, SupervisorProfile
from common.models import Department, Tag

User = get_user_model()

class UserCreateEndpointTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.department_it = Department.objects.create(name="Wydział IT")
        self.department_el = Department.objects.create(name="Wydział EL")

        self.coordinator_password = 'coordinator_password'
        self.user_coordinator_it = User.objects.create_user(
            username='coordinator_it', password=self.coordinator_password, email='k.it@example.com',
            first_name='Koordynator', last_name='IT', role=Role.COORDINATOR,
            description='Koordynator IT', department=self.department_it
        )

        self.user_coordinator_el = User.objects.create_user(
            username='coordinator_el', password=self.coordinator_password, email='k.el@example.com',
            first_name='Koordynator', last_name='EL', role=Role.COORDINATOR,
            description='Koordynator EL', department=self.department_el
        )

        self.user_coordinator_no_dept = User.objects.create_user(
            username='coordinator_no_dept', password=self.coordinator_password, email='k.nodept@example.com',
            first_name='Koordynator', last_name='BrakDzialu', role=Role.COORDINATOR,
            description='Koordynator bez działu', department=None
        )


        self.student_password = 'student_password'
        self.user_student = User.objects.create_user(
            username='student_test', password=self.student_password, email='s.test@example.com',
            first_name='Student', last_name='Testowy', role=Role.STUDENT,
            description='Initial student description', department=self.department_it
        )

        self.supervisor_password = 'supervisor_password'
        self.user_supervisor_it = User.objects.create_user(
            username='supervisor_it', password=self.supervisor_password, email='p.it@example.com',
            first_name='Promotor', last_name='IT', role=Role.SUPERVISOR,
            academic_title=AcademicTitle.DOCTOR, description='Initial supervisor IT description',
            department=self.department_it
        )

        self.admin_password = 'admin_password'
        self.user_admin = User.objects.create_superuser(
            username='admin_test', password=self.admin_password, email='a.test@example.com',
            first_name='Admin', last_name='Testowy', role=Role.ADMIN,
            description='Initial admin description', department=self.department_it
        )

        self.create_url = reverse('create-single-user')

    def test_create_user_unauthenticated(self):
        data = {
            'email': 'new_student@example.com',
            'first_name': 'Nowy',
            'last_name': 'Student',
            'academic_title': AcademicTitle.NONE,
            'role': Role.STUDENT,
            'index_number': 'S98765'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_by_student(self):
        self.client.force_authenticate(user=self.user_student)
        data = {
            'email': 'new_student_by_student@example.com',
            'first_name': 'Nowy',
            'last_name': 'Student',
            'academic_title': AcademicTitle.NONE,
            'role': Role.STUDENT,
            'index_number': 'S98766'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_by_supervisor(self):
        self.client.force_authenticate(user=self.user_supervisor_it)
        data = {
            'email': 'new_student_by_supervisor@example.com',
            'first_name': 'Nowy',
            'last_name': 'Student',
            'academic_title': AcademicTitle.NONE,
            'role': Role.STUDENT,
            'index_number': 'S98767'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_user_by_admin(self):
        self.client.force_authenticate(user=self.user_admin)
        data = {
            'email': 'new_student_by_admin@example.com',
            'first_name': 'Nowy',
            'last_name': 'Student',
            'academic_title': AcademicTitle.NONE,
            'role': Role.STUDENT,
            'index_number': 'S98768'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_student_by_coordinator(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        data = {
            'email': 'new_student_by_coord@example.com',
            'first_name': 'Nowy',
            'last_name': 'StudentKoord',
            'academic_title': AcademicTitle.NONE,
            'role': Role.STUDENT,
            'index_number': 'S98769'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_user = User.objects.get(email='new_student_by_coord@example.com')
        self.assertEqual(created_user.role, Role.STUDENT)
        self.assertEqual(created_user.first_name, 'Nowy')
        self.assertEqual(created_user.last_name, 'StudentKoord')
        self.assertEqual(created_user.department, self.user_coordinator_it.department)
        self.assertIsNotNone(created_user.studentprofile)
        self.assertEqual(created_user.studentprofile.index_number, 'S98769')
        self.assertIsNotNone(created_user.username)
        self.assertIsNotNone(created_user.password)
        # Poprawiona asercja dla tytułu naukowego studenta
        self.assertEqual(created_user.academic_title, AcademicTitle.NONE)

        self.assertIn('user', response.data)
        self.assertIn('index_number', response.data)
        self.assertEqual(response.data['index_number'], 'S98769')
        self.assertEqual(response.data['user']['email'], 'new_student_by_coord@example.com')


    def test_create_supervisor_by_coordinator(self):
        self.client.force_authenticate(user=self.user_coordinator_el)
        data = {
            'email': 'new_supervisor_by_coord@example.com',
            'first_name': 'Nowy',
            'last_name': 'PromotorKoord',
            'academic_title': AcademicTitle.DOCTOR,
            'role': Role.SUPERVISOR,
            'index_number': ''
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_user = User.objects.get(email='new_supervisor_by_coord@example.com')
        self.assertEqual(created_user.role, Role.SUPERVISOR)
        self.assertEqual(created_user.first_name, 'Nowy')
        self.assertEqual(created_user.last_name, 'PromotorKoord')
        self.assertEqual(created_user.department, self.user_coordinator_el.department)
        self.assertIsNotNone(created_user.supervisorprofile)
        self.assertEqual(created_user.academic_title, AcademicTitle.DOCTOR)
        self.assertIsNotNone(created_user.username)
        self.assertIsNotNone(created_user.password)

        self.assertIn('user', response.data)
        self.assertIn('academic_title', response.data['user'])
        self.assertEqual(response.data['user']['academic_title'], AcademicTitle.DOCTOR)
        self.assertNotIn('index_number', response.data)


    def test_create_user_coordinator_no_department(self):
        self.client.force_authenticate(user=self.user_coordinator_no_dept)
        data = {
            'email': 'student_no_dept_coord@example.com',
            'first_name': 'Student',
            'last_name': 'NoDept',
            'academic_title': AcademicTitle.NONE,
            'role': Role.STUDENT,
            'index_number': 'S11223'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_user_missing_required_fields(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        data = {
            'email': 'invalid_user@example.com',
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('role', response.data)
        self.assertIn('academic_title', response.data)

    def test_create_user_duplicate_email(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        User.objects.create(email='duplicate_email_test_3@example.com', username='temp_dup_email_3', password='temp_password', first_name='Temp', last_name='User', role=Role.STUDENT, department=self.department_it)

        data = {
            'email': 'duplicate_email_test_3@example.com',
            'first_name': 'Duplicate',
            'last_name': 'Email',
            'academic_title': AcademicTitle.NONE,
            'role': Role.STUDENT,
            'index_number': 'S11227'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertIn("Użytkownik o adresie email 'duplicate_email_test_3@example.com' już istnieje.", response.data['detail'])


    def test_create_user_duplicate_username(self):
        self.client.force_authenticate(user=self.user_coordinator_it)
        User.objects.create(username='nowypromotorkoord_dup', password='temp_password', email='temp_user_dup_username4@example.com', first_name='Temp', last_name='User', role=Role.STUDENT, department=self.department_it)

        data = {
            'email': 'another_new_supervisor4@example.com',
            'first_name': 'Nowy',
            'last_name': 'PromotorKoord',
            'academic_title': AcademicTitle.DOCTOR,
            'role': Role.SUPERVISOR,
            'index_number': ''
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_user = User.objects.get(email='another_new_supervisor4@example.com')
        self.assertNotEqual(created_user.username, 'nowypromotorkoord_dup')
        self.assertTrue(created_user.username.startswith('nowypromotorkoord'))