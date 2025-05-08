from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from common.models import Department, Tag
from users.models import User, Role, AcademicTitle
from common.search_service import SearchService

class UserSearchAPITest(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username="testuser", password="testpassword")
        response = self.client.post('/auth/login/', {
            'username': 'testuser',
            'password': 'testpassword'
        })

        self.token = response.data['access']

        self.department_1 = Department.objects.create(name="Wydział A")
        self.department_2 = Department.objects.create(name="Wydział B")
        self.department_3 = Department.objects.create(name="Wydział AC")

        tag_python = Tag.objects.create(name="Python")
        tag_ml = Tag.objects.create(name="ML")
        tag_math = Tag.objects.create(name="Math")
        tag_java = Tag.objects.create(name="Java")

        self.student_1 = User.objects.create_user(
            username="adam",
            first_name="Adam",
            last_name="Ogórek",
            role=Role.STUDENT,
            department = self.department_1,
        )

        self.student_1.tags.add(tag_python)
        self.student_1.tags.add(tag_ml)

        self.student_2 = User.objects.create_user(
            username="Benedykt",
            first_name="Benedykt",
            last_name="Borowski",
            role=Role.STUDENT,
            department = self.department_1,
        ) 

        self.student_2.tags.add(tag_java)

        self.student_3 = User.objects.create_user(
            username="Czesio",
            first_name="Czesław",
            last_name="Ogórek",
            role=Role.STUDENT,
            department = self.department_2,
        )

        self.student_3.tags.add(tag_math)

        self.student_4 = User.objects.create_user(
            username="Dominika",
            first_name="Dominika",
            last_name="Dębowa",
            role=Role.STUDENT,
            department = self.department_3,
        )

        self.supervisor_1 = User.objects.create_user(
            username="Zygmunt",
            first_name="Zygmunt",
            academic_title=AcademicTitle.PROFESSOR,
            role=Role.SUPERVISOR,
            department = self.department_1,
        )

        self.supervisor_1.tags.add(tag_math)
        self.supervisor_1.tags.add(tag_ml)

        self.supervisor_2 = User.objects.create_user(
            username="Włodzimierz",
            first_name="Włodzimierz",
            last_name="Ogórek",
            academic_title=AcademicTitle.PROFESSOR,
            role=Role.SUPERVISOR,
            department = self.department_2,
        )

        self.supervisor_2.tags.add(tag_java)
        self.supervisor_2.tags.add(tag_ml)

        self.supervisor_3 = User.objects.create_user(
            username="Ula",
            first_name="Urszula",
            academic_title=AcademicTitle.DOCTOR,
            role=Role.SUPERVISOR,
            department = self.department_3,
        )
        
        self.supervisor_4 = User.objects.create_user(
            username="Tadek",
            first_name="Tadeusz",
            academic_title=AcademicTitle.MASTER,
            role=Role.SUPERVISOR,
            department = self.department_3,
        )

        self.supervisor_4.tags.add(tag_python)
        self.supervisor_4.tags.add(tag_ml)
        self.supervisor_4.tags.add(tag_math)

        self.search_service = SearchService()

    def test_search_by_name(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/common/search-users/', {"last_name": "Ogórek"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  

        names = [user['first_name'] for user in response.data]
        self.assertIn("Adam", names)
        self.assertIn("Czesław", names)
        self.assertIn("Włodzimierz", names)

    def test_search_by_tags(self):
        response = self.client.get('/common/search-users/', {"tags": ["ML", "Math"]}, HTTP_AUTHORIZATION=f'JWT {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data

        expected_order = [
            self.supervisor_1, 
            self.supervisor_4,
            self.supervisor_2,
            self.student_1,
            self.student_3,
        ]

        self.assertEqual(len(results), 5)

        for i, (expected, recieved) in enumerate(zip(expected_order, results)):
            self.assertEqual(expected.username, recieved['username'], f"Problem with {i}th element")