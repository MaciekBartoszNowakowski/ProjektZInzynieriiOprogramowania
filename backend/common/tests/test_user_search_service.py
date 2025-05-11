from django.test import TestCase
from common.models import Department, Tag
from users.models import User, Role, AcademicTitle
from common.search_service import SearchService

class TestUserSearchService(TestCase):
    def setUp(self):
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

    def test_filtering_by_first_name(self):
        results = self.search_service.search_user(first_name="Adam")

        self.assertEqual(results.count(), 1)
        self.assertIn(self.student_1, results)

    def test_filtering_by_last_name(self):
        results = self.search_service.search_user(last_name="Ogórek")

        self.assertEqual(results.count(), 3)
        self.assertIn(self.student_1, results)
        self.assertIn(self.student_3, results)
        self.assertIn(self.supervisor_2, results)

    def test_filtering_by_first_name_and_last_name(self):
        results = self.search_service.search_user(first_name="Włodzimierz", last_name="Ogórek")

        self.assertEqual(results.count(), 1)
        self.assertIn(self.supervisor_2, results)

    def test_filtering_by_department(self):
        results = self.search_service.search_user(department="Wydział A", sort_by=None, limit=1000)

        self.assertEqual(results.count(), 3)
        self.assertIn(self.student_1, results)
        self.assertIn(self.student_2, results)
        self.assertIn(self.supervisor_1, results)

    def test_filtering_by_tag(self):
        results = self.search_service.search_user(tags=["Math"], sort_by=["username"], orders=["asc"], limit=1000, offset=0)

        expected_order = [
            self.student_3,
            self.supervisor_4,
            self.supervisor_1,
        ]

        self.assertEqual(results.count(), 3)

        for i, (expected, recieved) in enumerate(zip(expected_order, results)):
            self.assertEqual(expected, recieved, f"Problem with {i}th element")

    def test_filtering_by_tags(self):
        results = self.search_service.search_user(tags=["Python", "ML"], sort_by=["username"], orders=["asc"], limit=1000, offset=0)

        expected_order = [
            self.student_1,
            self.supervisor_4,
            self.supervisor_2,
            self.supervisor_1,
        ]

        self.assertEqual(results.count(), 4)

        for i, (expected, recieved) in enumerate(zip(expected_order, results)):
            self.assertEqual(expected, recieved, f"Problem with {i}th element")

    def test_filtering_by_role(self):
        results = self.search_service.search_user(role="student", limit=1000)

        expected_values = [
            self.student_1,
            self.student_2,
            self.student_3,
            self.student_4,
        ]

        self.assertEqual(results.count(), 4)

        for expected_value in expected_values:
            self.assertIn(expected_value, results)

        results = self.search_service.search_user(role="supervisor", limit=1000)

        expected_values = [
            self.supervisor_1,
            self.supervisor_2,
            self.supervisor_3,
            self.supervisor_4,
        ]

        self.assertEqual(results.count(), 4)

        for expected_value in expected_values:
            self.assertIn(expected_value, results)

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

        for i, (expected, recieved) in enumerate(zip(expected_order, results)):
            self.assertEqual(expected, recieved, f"Problem with {i}th element")

    def test_sorting_titles(self):
        results = self.search_service.search_user(sort_by=["academic_title", "first_name"], orders=["desc", "asc"], limit=1000, offset=0)

        expected_order = [
            self.supervisor_2, 
            self.supervisor_1,
            self.supervisor_3,
            self.supervisor_4,
            self.student_1,
            self.student_2,
            self.student_3,
            self.student_4,
        ]

        self.assertEqual(results.count(), 8)

        for i, (expected, recieved) in enumerate(zip(expected_order, results)):
            self.assertEqual(expected, recieved, f"Problem with {i}th element")

    def test_sorting_tag_count(self):
        results = self.search_service.search_user(tags=["Math", "ML"], sort_by=["matching_tag_count", "academic_title", "last_name"], orders=["desc", "desc", "asc"], limit=1000, offset=0)

        expected_order = [
            self.supervisor_1, 
            self.supervisor_4,
            self.supervisor_2,
            self.student_1,
            self.student_3,
        ]

        self.assertEqual(results.count(), 5)

        for i, (expected, recieved) in enumerate(zip(expected_order, results)):
            self.assertEqual(expected, recieved, f"Problem with {i}th element")

    def test_pagination(self):
        results = self.search_service.search_user(sort_by=["department", "username"], orders=["asc", "desc"], limit=3, offset=1)

        expected_order = [
            self.student_2,
            self.student_1,
            self.supervisor_2,
        ]

        self.assertEqual(results.count(), 3)

        for i, (expected, recieved) in enumerate(zip(expected_order, results)):
            self.assertEqual(expected, recieved, f"Problem with {i}th element")

    def test_pagination_end(self):
        results = self.search_service.search_user(sort_by=["department", "username"], orders=["asc", "desc"], limit=5, offset=6)

        expected_order = [
            self.supervisor_4,
            self.student_4,
        ]

        self.assertEqual(results.count(), 2)
        
        for i, (expected, recieved) in enumerate(zip(expected_order, results)):
            self.assertEqual(expected, recieved, f"Problem with {i}th element")