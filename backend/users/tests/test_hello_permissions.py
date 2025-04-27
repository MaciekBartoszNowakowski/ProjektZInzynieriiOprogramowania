from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from parameterized import parameterized
from users.models import Role

User = get_user_model()

class HelloWorldViewPermissionTests(APITestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(username='student', password='password123')
        self.student_user.role = Role.STUDENT
        self.student_user.save()

        self.supervisor_user = User.objects.create_user(username='supervisor', password='password123')
        self.supervisor_user.role = Role.SUPERVISOR
        self.supervisor_user.save()

        self.coordinator_user = User.objects.create_user(username='coordinator', password='password123')
        self.coordinator_user.role = Role.COORDINATOR
        self.coordinator_user.save()

        self.admin_user = User.objects.create_user(username='admin', password='password123')
        self.admin_user.role = Role.ADMIN
        self.admin_user.save()

        self.anonymous_user = None

        self.users = {
            'student': self.student_user,
            'supervisor': self.supervisor_user,
            'coordinator': self.coordinator_user,
            'admin': self.admin_user,
            'anonymous': self.anonymous_user,
        }

        self.view_details = {
            'hello-world': {'url_name': 'hello_world', 'greeting': 'Hello, World!'},
            'hello-student': {'url_name': 'hello_world_student', 'greeting': 'Hello, Student!'},
            'hello-supervisor': {'url_name': 'hello_world_supervisor', 'greeting': 'Hello, Supervisor!'},
            'hello-coordinator': {'url_name': 'hello_world_coordinator', 'greeting': 'Hello, Coordinator!'},
            'hello-admin': {'url_name': 'hello_world_admin', 'greeting': 'Hello, Admin!'},
            'hello-student-or-supervisor': {'url_name': 'hello_world_student_or_supervisor', 'greeting': 'Hello, Student or Supervisor!'},
        }

    @parameterized.expand([
        ("student_view_by_student", "hello-student", "student", status.HTTP_200_OK),
        ("supervisor_view_by_supervisor", "hello-supervisor", "supervisor", status.HTTP_200_OK),
        ("coordinator_view_by_coordinator", "hello-coordinator", "coordinator", status.HTTP_200_OK),
        ("admin_view_by_admin", "hello-admin", "admin", status.HTTP_200_OK),
        ("student_or_supervisor_view_by_student", "hello-student-or-supervisor", "student", status.HTTP_200_OK),
        ("student_or_supervisor_view_by_supervisor", "hello-student-or-supervisor", "supervisor", status.HTTP_200_OK),
        ("hello_world_by_anonymous", "hello-world", "anonymous", status.HTTP_200_OK),
        ("hello_world_by_student", "hello-world", "student", status.HTTP_200_OK),
    ])
    def test_view_access_granted(self, name, view_key, user_key, expected_status):
        user = self.users[user_key]
        details = self.view_details[view_key]
        url = reverse(details['url_name'])
        expected_greeting = details['greeting']

        if user:
            self.client.force_authenticate(user=user)
        else:
            self.client.logout()

        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_status, f"Test failed for: {name} - Status Code")

        if expected_status == status.HTTP_200_OK:
            self.assertIn('data', response.data, f"Test failed for: {name} - Missing 'data' key")
            self.assertIsInstance(response.data.get('data'), dict, f"Test failed for: {name} - 'data' is not a dict")
            self.assertIn('greeting', response.data.get('data', {}), f"Test failed for: {name} - Missing 'greeting' key in 'data'")
            self.assertEqual(response.data['data']['greeting'], expected_greeting, f"Test failed for: {name} - Incorrect Greeting")

    @parameterized.expand([
        ("student_view_by_supervisor", "hello-student", "supervisor", status.HTTP_403_FORBIDDEN),
        ("student_view_by_anonymous", "hello-student", "anonymous", status.HTTP_401_UNAUTHORIZED),
        ("supervisor_view_by_student", "hello-supervisor", "student", status.HTTP_403_FORBIDDEN),
        ("supervisor_view_by_anonymous", "hello-supervisor", "anonymous", status.HTTP_401_UNAUTHORIZED),
        ("coordinator_view_by_student", "hello-coordinator", "student", status.HTTP_403_FORBIDDEN),
        ("coordinator_view_by_anonymous", "hello-coordinator", "anonymous", status.HTTP_401_UNAUTHORIZED),
        ("admin_view_by_student", "hello-admin", "student", status.HTTP_403_FORBIDDEN),
        ("admin_view_by_anonymous", "hello-admin", "anonymous", status.HTTP_401_UNAUTHORIZED),
        ("student_or_supervisor_view_by_coordinator", "hello-student-or-supervisor", "coordinator", status.HTTP_403_FORBIDDEN),
        ("student_or_supervisor_view_by_admin", "hello-student-or-supervisor", "admin", status.HTTP_403_FORBIDDEN),
        ("student_or_supervisor_view_by_anonymous", "hello-student-or-supervisor", "anonymous", status.HTTP_401_UNAUTHORIZED),
    ])
    def test_view_access_denied(self, name, view_key, user_key, expected_status):
        user = self.users[user_key]
        details = self.view_details[view_key]
        url = reverse(details['url_name'])

        if user:
            self.client.force_authenticate(user=user)
        else:
            self.client.logout()

        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_status, f"Test failed for: {name} - Incorrect Status Code")
