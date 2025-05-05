from django.test import TestCase
from common.models import Department
from users.models import User, Role
from common.search_service import SearchService

class TestSearchService(TestCase):
    def setUp(self):
        self.department_1 = Department.objects.create(name="Wydział A")
        self.department_2 = Department.objects.create(name="Wydział B")
        self.department_3 = Department.objects.create(name="Wydział C")

        self.student_1 = User.objects.create_user(
            username="adam",
            role=Role.STUDENT,
            department = self.department_1,
        )

        self.student_2 = User.objects.create_user(
            username="Benedykt",
            role=Role.STUDENT,
            department = self.department_1,
        ) 

        self.student_3 = User.objects.create_user(
            username="Czesław",
            role=Role.STUDENT,
            department = self.department_2,
        )

        self.student_4 = User.objects.create_user(
            username="Dominika",
            role=Role.STUDENT,
            department = self.department_3,
        )

        self.supervisor_1 = User.objects.create_user(
            username="Zygmunt",
            role=Role.SUPERVISOR,
            department = self.department_1,
        )

        self.supervisor_2 = User.objects.create_user(
            username="Włodzimierz",
            role=Role.SUPERVISOR,
            department = self.department_2,
        )

        self.supervisor_3 = User.objects.create_user(
            username="Urszula",
            role=Role.SUPERVISOR,
            department = self.department_3,
        )
        
        self.supervisor_4 = User.objects.create_user(
            username="Tadeusz",
            role=Role.SUPERVISOR,
            department = self.department_3,
        )

        self.search_service = SearchService()

    def test_filtering_by_department(self):
        results = self.search_service.search_user(department="Wydział A", sort_by=None, limit=1000)

        self.assertEqual(results.count(), 3)
        self.assertIn(self.student_1, results)
        self.assertIn(self.student_2, results)
        self.assertIn(self.supervisor_1, results)