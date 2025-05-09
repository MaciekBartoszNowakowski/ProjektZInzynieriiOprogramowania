from django.test import TestCase
from common.models import Department, Tag
from users.models import User, Role, AcademicTitle
from thesis.models import Thesis, ThesisStatus, ThesisType
from thesis.services.thesis_service import *

class TestThesisService(TestCase):
    def setUp(self):
        self.department_1 = Department.objects.create(name="Wydział A")
        self.department_2 = Department.objects.create(name="Wydział B")
        self.department_3 = Department.objects.create(name="Wydział AC")

        tag_python = Tag.objects.create(name="Python")
        tag_ml = Tag.objects.create(name="ML")
        tag_math = Tag.objects.create(name="Math")
        tag_java = Tag.objects.create(name="Java")
        tag_graph = Tag.objects.create(name="Graph Algs")

        self.supervisor_1 = User.objects.create_user(
            username="Zygmunt",
            first_name="Zygmunt",
            last_name="Anna",
            academic_title=AcademicTitle.PROFESSOR,
            role=Role.SUPERVISOR,
            department = self.department_1,
        )

        self.supervisor_1.tags.add(tag_math)
        self.supervisor_1.tags.add(tag_ml)

        self.supervisor_2 = User.objects.create_user(
            username="Włodzimierz",
            first_name="Włodzimierz",
            last_name="Biały",
            academic_title=AcademicTitle.DOCTOR,
            role=Role.SUPERVISOR,
            department = self.department_2,
        )

        self.supervisor_2.tags.add(tag_java)
        self.supervisor_2.tags.add(tag_ml)

        self.supervisor_3 = User.objects.create_user(
            username="Ula",
            first_name="Urszula",
            last_name="Aleigo",
            academic_title=AcademicTitle.HABILITATED_DOCTOR,
            role=Role.SUPERVISOR,
            department = self.department_3,
        )

        self.supervisor_3.tags.add(tag_python)
        self.supervisor_3.tags.add(tag_graph)
        
        self.supervisor_4 = User.objects.create_user(
            username="Tadek",
            first_name="Tadeusz",
            last_name="Pomorski",
            academic_title=AcademicTitle.MASTER,
            role=Role.SUPERVISOR,
            department = self.department_3,
        )

        self.supervisor_4.tags.add(tag_python)
        self.supervisor_4.tags.add(tag_ml)
        self.supervisor_4.tags.add(tag_math)

        self.thesis_service = ThesisService()

    def test_adding_thesis_invalid_supervisor_id(self):
        with self.assertRaises(InvalidSupervisorIdException):
            self.thesis_service.add_new_thesis(
                supervisor_id=self.supervisor_1.pk +\
                    self.supervisor_2.pk +\
                    self.supervisor_3.pk +\
                    self.supervisor_4.pk,
                thesis_type=ThesisType.ENGINEERING,
                name="Wizualizacja przepływu gradientów w sieci neuronowej",
                max_students=3
            )

    def test_adding_thesis_invalid_type(self):
        with self.assertRaises(InvalidThesisTypeException):
            self.thesis_service.add_new_thesis(
                supervisor_id=self.supervisor_1.pk,
                thesis_type="HABILITATION",
                name="Bardzo poważna praca",
                max_students=10
            )

    def test_adding_thesis_limit_exceeded(self):
        with self.assertRaises(ThesisTypeLimitExceededException):
            # zmiana limitu dla dr. Włodzimierza
            self.supervisor_2.bacherol_limit = 0

            self.thesis_service.add_new_thesis(
                supervisor_id=self.supervisor_2.pk,
                thesis_type=ThesisType.BACHELOR,
                name="Struktury chemiczne substancji opisane w języku Java",
                max_students=1,
                language="Polish"
            )

    def test_adding_thesis_nonpositive_max_students(self):
        with self.assertRaises(NonPositiveStudentsLimitException):
            self.thesis_service.add_new_thesis(
                supervisor_id=self.supervisor_4.pk,
                thesis_type=ThesisType.ENGINEERING,
                name="Wizualizacja przepływu gradientów w sieci neuronowej",
                max_students=-3
            )

    def test_adding_thesis(self):
        # zmiana limitu dla dr. Włodzimierza
        self.supervisor_2.bacherol_limit = 1

        self.thesis_service.add_new_thesis(
            supervisor_id=self.supervisor_4.pk,
            thesis_type=ThesisType.ENGINEERING,
            name="Wizualizacja przepływu gradientów w sieci neuronowej",
            max_students=3
        )

        self.thesis_service.add_new_thesis(
            supervisor_id=self.supervisor_2.pk,
            thesis_type=ThesisType.BACHELOR,
            name="Struktury chemiczne substancji opisane w języku Java",
            max_students=1,
            language="Polish"
        )

        self.thesis_service.add_new_thesis(
            supervisor_id=self.supervisor_1.pk,
            thesis_type=ThesisType.MASTER,
            name="Przechowywanie skompresowanych gradientów i zależności matematycznych w systemie bazodanowym",
            max_students=2
        )

        self.thesis_service.add_new_thesis(
            supervisor_id=self.supervisor_3.pk,
            thesis_type=ThesisType.DOCTOR,
            name="Zastosowanie algorytmów grafowych w bioinformatyce i leczeniu nowotworów",
            language="Spanish"
        )

        self.assertEqual(Thesis.objects.all().count(), 4)

    def test_getting_all_available_theses(self):
        available_theses = self.thesis_service.get_available_theses()
        self.assertEqual(available_theses.count(), 4)
