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
            first_name="Adam",
            role=Role.STUDENT,
            department = self.department_1,
        )

        self.student_2 = User.objects.create_user(
            username="Benedykt",
            first_name="Benedykt",
            role=Role.STUDENT,
            department = self.department_1,
        ) 

        self.student_3 = User.objects.create_user(
            username="Czesio",
            first_name="Czesław",
            role=Role.STUDENT,
            department = self.department_2,
        )

        self.student_4 = User.objects.create_user(
            username="Dominika",
            first_name="Dominika",
            role=Role.STUDENT,
            department = self.department_3,
        )

        self.supervisor_1 = User.objects.create_user(
            username="Zygmunt",
            first_name="Zygmunt",
            role=Role.SUPERVISOR,
            department = self.department_1,
        )

        self.supervisor_2 = User.objects.create_user(
            username="Włodzimierz",
            first_name="Włodzimierz",
            role=Role.SUPERVISOR,
            department = self.department_2,
        )

        self.supervisor_3 = User.objects.create_user(
            username="Ula",
            first_name="Urszula",
            role=Role.SUPERVISOR,
            department = self.department_3,
        )
        
        self.supervisor_4 = User.objects.create_user(
            username="Tadek",
            first_name="Tadeusz",
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

    def test_sorting(self):
        results = self.search_service.search_user(sort_by=["department", "username"], orders=["asc", "desc"], limit=1000)

        expected_order = [
            self.supervisor_1, 
            self.student_2,
            self.student_1,
            self.supervisor_2,
            self.student_3,
            self.supervisor_3,
            self.supervisor_4,
            self.student_4,
            ]

        self.assertEqual(results.count(), 8)
        print(results)

        for i, (expected, recieved) in enumerate(zip(expected_order, results)):
            self.assertEqual(expected, recieved, f"Problem with {i}th element")

