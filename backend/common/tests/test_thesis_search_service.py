from django.test import TestCase
from common.models import Department, Tag
from users.models import User, Role, AcademicTitle, SupervisorProfile
from common.search_service import SearchService
from thesis.models import Thesis, ThesisType, ThesisStatus

class TestUserSearchService(TestCase):
    def setUp(self):
        self.department_1 = Department.objects.create(name="Wydział A")
        self.department_2 = Department.objects.create(name="Wydział B")
        self.department_3 = Department.objects.create(name="Wydział AC")

        tag_python = Tag.objects.create(name="Python")
        tag_ml = Tag.objects.create(name="ML")
        tag_math = Tag.objects.create(name="Math")
        tag_java = Tag.objects.create(name="Java")

        self.supervisor_1 = User.objects.create_user(
            username="Zygmunt",
            first_name="Zygmunt",
            academic_title=AcademicTitle.PROFESSOR,
            role=Role.SUPERVISOR,
            department = self.department_1,
        )

        supervisor_profile = SupervisorProfile.objects.create(user=self.supervisor_1)

        self.supervisor_1.tags.add(tag_math)
        self.supervisor_1.tags.add(tag_ml)


        self.supervisor_2 = User.objects.create_user(
            username="Włodzimierz",
            first_name="Włodzimierz",
            last_name="Ogórek",
            academic_title=AcademicTitle.MASTER,
            role=Role.SUPERVISOR,
            department = self.department_2,
        )

        self.supervisor_2.tags.add(tag_java)
        self.supervisor_2.tags.add(tag_ml)

        SupervisorProfile.objects.create(user=self.supervisor_2)

        self.thesis1 = Thesis.objects.create(
            supervisor_id=self.supervisor_1.supervisorprofile,
            thesis_type=ThesisType.ENGINEERING,
            name="Matematyczny Python",
            max_students=1,
            status=ThesisStatus.APP_OPEN,
            language="Polski"
        )

        self.thesis1.tags.add(tag_math)
        self.thesis1.tags.add(tag_python)

        self.thesis2 = Thesis.objects.create(
        supervisor_id = self.supervisor_1.supervisorprofile,
        thesis_type = ThesisType.MASTER,
        name = "Potężny ML",
        max_students = 1,
        status=ThesisStatus.APP_OPEN,
        language="Polski",
        )

        self.thesis2.tags.add(tag_ml)

        self.thesis3 = Thesis.objects.create(
            supervisor_id = self.supervisor_1.supervisorprofile,
            thesis_type = ThesisType.ENGINEERING,
            name = "Matematyczna Java MLowa",
            max_students = 1,
            status=ThesisStatus.APP_OPEN,
            language="Polski",
        )

        self.thesis3.tags.add(tag_ml)
        self.thesis3.tags.add(tag_java)
        self.thesis3.tags.add(tag_math)

        self.thesis4 = Thesis.objects.create(
            supervisor_id = self.supervisor_2.supervisorprofile,
            thesis_type = ThesisType.ENGINEERING,
            name = "Jython 2.0",
            max_students = 1,
            status=ThesisStatus.APP_OPEN,
            language="Polski",
        )

        self.thesis4.tags.add(tag_java)
        self.thesis4.tags.add(tag_python)

        self.thesis5 = Thesis.objects.create(
            supervisor_id = self.supervisor_2.supervisorprofile,
            thesis_type = ThesisType.ENGINEERING,
            name = "Matematyczne Oblicza Javy (i Pythona)",
            max_students = 1,
            status=ThesisStatus.APP_OPEN,
            language="Polski",
        )

        self.thesis5.tags.add(tag_java)
        self.thesis5.tags.add(tag_math)
        self.thesis5.tags.add(tag_python)


        self.search_service = SearchService()

    def test_filter_by_tags(self):
        results = self.search_service.search_topics(tags=["Python", "Math"], limit=1000, offset=0)

        expected_values = [
            self.thesis1,
            self.thesis3,
            self.thesis4,
            self.thesis5,
        ]

        self.assertEqual(results.count(), 4)

        for expected_value in expected_values:
            self.assertIn(expected_value, results)

    def test_filter_by_department(self):
        results = self.search_service.search_topics(department="Wydział A", limit=1000, offset=0)

        expected_values = [
            self.thesis1,
            self.thesis2,
            self.thesis3,
        ]
        self.assertEqual(results.count(), 3)

        for expected_value in expected_values:
            self.assertIn(expected_value, results)

    def test_filter_by_thesis_type(self):
        results = self.search_service.search_topics(thesis_type="ENGINEERING", limit=1000, offset=0)

        expected_values = [
            self.thesis1,
            self.thesis3,
            self.thesis4,
            self.thesis5,
        ]
        self.assertEqual(results.count(), 4)

        for expected_value in expected_values:
            self.assertIn(expected_value, results)

    def test_sorting_by_thesis_type(self):
        results = self.search_service.search_topics(sort_by=["thesis_type", "academic_title"], orders=["asc", "asc"], limit=100)

        expected_order = [
            self.thesis4, 
            self.thesis5,
            self.thesis1, 
            self.thesis3, 
            self.thesis2,
        ]
        self.assertEqual(results.count(), len(expected_order))

        for i, (expected, recieved) in enumerate(zip(expected_order, results)):
            self.assertEqual(expected, recieved, f"Problem with {i}th element")

    def test_sorting_by_tags_and_title(self):
        results = self.search_service.search_topics(tags=["Python", "Math", "Java"], sort_by=["matching_tag_count", "academic_title"], orders=["desc", "desc"], limit=100)

        expected_order = [
            self.thesis5, 
            self.thesis1,
            self.thesis3, 
            self.thesis4,
        ]
        self.assertEqual(results.count(), len(expected_order))

        for i, (expected, recieved) in enumerate(zip(expected_order, results)):
            self.assertEqual(expected, recieved, f"Problem with {i}th element")