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

        self.tag_python = Tag.objects.create(name="Python")
        self.tag_ml = Tag.objects.create(name="ML")
        self.tag_math = Tag.objects.create(name="Math")
        self.tag_java = Tag.objects.create(name="Java")
        self.tag_graph = Tag.objects.create(name="Graph Algs")

        self.supervisor_1 = SupervisorProfile.objects.create(
            user=User.objects.create_user(
                username="Zygmunt",
                first_name="Zygmunt",
                last_name="Anna",
                academic_title=AcademicTitle.PROFESSOR,
                role=Role.SUPERVISOR,
                department = self.department_1,
            )
        )

        self.supervisor_1.user.tags.add(self.tag_math)
        self.supervisor_1.user.tags.add(self.tag_ml)

        self.supervisor_2 = SupervisorProfile.objects.create(
            user=User.objects.create_user(
                username="Włodzimierz",
                first_name="Włodzimierz",
                last_name="Biały",
                academic_title=AcademicTitle.DOCTOR,
                role=Role.SUPERVISOR,
                department = self.department_2,
            )
        )

        self.supervisor_2.user.tags.add(self.tag_java)
        self.supervisor_2.user.tags.add(self.tag_ml)

        self.supervisor_3 = SupervisorProfile.objects.create(
            user=User.objects.create_user(
                username="Ula",
                first_name="Urszula",
                last_name="Aleigo",
                academic_title=AcademicTitle.HABILITATED_DOCTOR,
                role=Role.SUPERVISOR,
                department = self.department_3,
            )
        )

        self.supervisor_3.user.tags.add(self.tag_python)
        self.supervisor_3.user.tags.add(self.tag_graph)
        
        self.supervisor_4 = SupervisorProfile.objects.create(
            user=User.objects.create_user(
                username="Tadek",
                first_name="Tadeusz",
                last_name="Pomorski",
                academic_title=AcademicTitle.MASTER,
                role=Role.SUPERVISOR,
                department = self.department_3,
            )
        )

        self.supervisor_4.user.tags.add(self.tag_python)
        self.supervisor_4.user.tags.add(self.tag_ml)
        self.supervisor_4.user.tags.add(self.tag_math)

        self.non_supervisor = User.objects.create_user(
            username="NaPewno",
            first_name="NieJestem",
            last_name="Promotorem",
            academic_title=AcademicTitle.ENGINEER,
            role=Role.STUDENT,
            department = self.department_1,
        )

        self.thesis_1 = Thesis.objects.create(
            supervisor_id=self.supervisor_4,
            thesis_type=ThesisType.ENGINEERING,
            name="Wizualizacja przepływu gradientów w sieci neuronowej",
            max_students=3
        )

        self.thesis_2 = Thesis.objects.create(
            supervisor_id=self.supervisor_2,
            thesis_type=ThesisType.BACHELOR,
            name="Struktury chemiczne substancji opisane w języku Java",
            max_students=1,
            language="Polish"
        )

        self.thesis_3 = Thesis.objects.create(
            supervisor_id=self.supervisor_1,
            thesis_type=ThesisType.MASTER,
            name="Przechowywanie skompresowanych gradientów i zależności matematycznych w systemie bazodanowym",
            max_students=2
        )

        self.thesis_4 = Thesis.objects.create(
            supervisor_id=self.supervisor_3,
            thesis_type=ThesisType.DOCTOR,
            name="Zastosowanie algorytmów grafowych w bioinformatyce i leczeniu nowotworów",
            language="Spanish"
        )   

        self.thesis_service = ThesisService()


    def test_adding_thesis_invalid_supervisor_id(self):
        with self.assertRaises(InvalidSupervisorIdException):
            self.thesis_service.add_new_thesis(
                supervisor=self.non_supervisor,
                validated_data = {
                    "thesis_type": ThesisType.ENGINEERING,
                    "name": "Wizualizacja przepływu gradientów w sieci neuronowej",
                    "max_students": 3,
                    "tags": { self.tag_python, self.tag_ml }
                }
            )


    def test_adding_thesis_invalid_type(self):
        with self.assertRaises(InvalidThesisTypeException):
            self.thesis_service.add_new_thesis(
                supervisor=self.supervisor_1,
                validated_data = {
                    "thesis_type": "HABILITATION",
                    "name": "Bardzo poważna praca",
                    "max_students": 10
                }
            )


    def test_adding_thesis_no_required_title(self):
        with self.assertRaises(SupervisorTitleRequiredException):
            self.thesis_service.add_new_thesis(
                supervisor=self.supervisor_4,
                validated_data = {
                    "thesis_type": ThesisType.DOCTOR,
                    "name": "Struktury chemiczne substancji opisane w języku Java",
                    "max_students": 1,
                    "language": "Polish",
                    "tags": { self.tag_java }
                }
            )


    def test_adding_thesis_limit_exceeded(self):
        with self.assertRaises(ThesisTypeLimitExceededException):
            # zmiana limitu dla dr. Włodzimierza
            self.supervisor_2.bacherol_limit = 0
            self.supervisor_2.save()

            self.thesis_service.add_new_thesis(
                supervisor=self.supervisor_2,
                validated_data = {
                    "thesis_type": ThesisType.BACHELOR,
                    "name": "Poważna praca",
                    "max_students": 5,
                    "language": "Francais"
                }
            )


    def test_adding_thesis_nonpositive_max_students(self):
        with self.assertRaises(NonPositiveStudentsLimitException):
            self.thesis_service.add_new_thesis(
                supervisor=self.supervisor_4,
                validated_data = {
                    "thesis_type": ThesisType.ENGINEERING,
                    "name": "Wizualizacja przepływu gradientów w sieci neuronowej",
                    "max_students": -3,
                    "tags": { self.tag_python, self.tag_ml }
                }
            )


    def test_adding_thesis_wrong_tag_type(self):
        with self.assertRaises(TypeError):
            self.thesis_service.add_new_thesis(
                supervisor=self.supervisor_4,
                validated_data = {
                    "thesis_type": ThesisType.ENGINEERING,
                    "name": "Wizualizacja przepływu gradientów w sieci neuronowej",
                    "max_students": 3,
                    "tags": { "Python", "ML" }
                }
            )


    def test_adding_thesis(self):
        thesis_1 = self.thesis_service.add_new_thesis(
            supervisor=self.supervisor_4,
            validated_data = {
                "thesis_type": ThesisType.ENGINEERING,
                "name": "Wizualizacja przepływu gradientów w sieci neuronowej",
                "max_students": 3,
                "tags": { self.tag_python, self.tag_ml }
            }
        )

        thesis_2 = self.thesis_service.add_new_thesis(
            supervisor=self.supervisor_2,
            validated_data = {
                "thesis_type": ThesisType.BACHELOR,
                "name": "Struktury chemiczne substancji opisane w języku Java",
                "max_students": 1,
                "language": "Polish",
                "tags": { self.tag_java }
            }
        )

        thesis_3 = self.thesis_service.add_new_thesis(
            supervisor=self.supervisor_1,
            validated_data = {
                "thesis_type": ThesisType.MASTER,
                "name": "Przechowywanie skompresowanych gradientów i zależności matematycznych w systemie bazodanowym",
                "max_students": 2
            }
        )

        thesis_4 = self.thesis_service.add_new_thesis(
            supervisor=self.supervisor_3,
            validated_data = {
                "thesis_type": ThesisType.DOCTOR,
                "name": "Zastosowanie algorytmów grafowych w bioinformatyce i leczeniu nowotworów",
                "language": "Spanish",
                "tags": { self.tag_graph }
            }   
        )

        self.assertEqual(Thesis.objects.all().count(), 8)


    def test_update_thesis_invalid_supervisor_id(self):
        with self.assertRaises(InvalidSupervisorIdException):
            self.thesis_service.update_thesis(
                supervisor=self.non_supervisor,
                thesis_pk=self.thesis_1.pk,
                validated_data = {
                    "name": "Wizualizacja przepływu gradientów w sieci neuronowej",
                    "status": ThesisStatus.APP_OPEN,
                    "tags": { self.tag_python, self.tag_ml }
                }
            )


    def test_update_thesis_invalid_thesis_id(self):
        with self.assertRaises(InvalidThesisIdException):
            self.thesis_service.update_thesis(
                supervisor=self.supervisor_4,
                thesis_pk=-1,
                validated_data = {
                    "name": "Wizualizacja przepływu gradientów w sieci neuronowej",
                    "status": ThesisStatus.APP_OPEN,
                    "tags": { self.tag_python, self.tag_ml }
                }
            )


    def test_update_thesis_invalid_thesis_id_for_supervisor(self):
        with self.assertRaises(InvalidThesisIdException):
            self.thesis_service.update_thesis(
                supervisor=self.supervisor_2,
                thesis_pk=self.thesis_1.pk,
                validated_data = {
                    "name": "Wizualizacja przepływu gradientów w sieci neuronowej",
                    "status": ThesisStatus.APP_OPEN,
                    "tags": { self.tag_python, self.tag_ml }
                }
            )


    def test_update_thesis_wrong_tag_type(self):
        with self.assertRaises(TypeError):
            self.thesis_service.update_thesis(
                supervisor=self.supervisor_4,
                thesis_pk=self.thesis_1.pk,
                validated_data = {
                    "thesis_type": ThesisType.ENGINEERING,
                    "name": "Wizualizacja przepływu gradientów w sieci neuronowej",
                    "max_students": 3,
                    "tags": { "Python", "ML" }
                }
            )


    def test_update_thesis_invalid_status(self):
        with self.assertRaises(InvalidThesisStatusException):
            self.thesis_service.update_thesis(
                supervisor=self.supervisor_1,
                thesis_pk=self.thesis_3.pk,
                validated_data = {
                    "name": "Bardzo poważna praca",
                    "status": "Nie ma proszę się rozejść"
                }
            )


    def test_update_thesis_nonpositive_max_students(self):
        with self.assertRaises(NonPositiveStudentsLimitException):
            self.thesis_service.update_thesis(
                supervisor=self.supervisor_4,
                thesis_pk=self.thesis_1.pk,
                validated_data = {
                    "name": "Wizualizacja przepływu gradientów w sieci neuronowej",
                    "status": ThesisStatus.APP_CLOSED,
                    "max_students": -3,
                    "tags": { self.tag_python, self.tag_ml }
                }
            )


    def test_update_thesis(self):
        self.thesis_service.update_thesis(
            supervisor=self.supervisor_4,
            thesis_pk=self.thesis_1.pk,
            validated_data = {
                "name": "Wizualizacja przepływu gradientów w sieci neuronowej",
                "status": ThesisStatus.APP_CLOSED,
                "language": "Polish"
            }
        )

        self.thesis_1.refresh_from_db()

        self.assertEqual(self.thesis_1.status, ThesisStatus.APP_CLOSED)
        self.assertEqual(self.thesis_1.language, "Polish")
        self.assertEqual(self.thesis_1.tags.count(), 0)
        self.assertEqual(Thesis.objects.all().count(), 4)


    def test_delete_thesis_invalid_supervisor_id(self):
        with self.assertRaises(InvalidSupervisorIdException):
            self.thesis_service.delete_thesis(
                supervisor=self.non_supervisor,
                thesis_pk=self.thesis_1.pk
            )


    def test_delete_thesis_invalid_thesis_id(self):
        with self.assertRaises(InvalidThesisIdException):
            self.thesis_service.delete_thesis(
                supervisor=self.supervisor_4,
                thesis_pk=-1
            )


    def test_delete_thesis_invalid_thesis_id_for_supervisor(self):
        with self.assertRaises(InvalidThesisIdException):
            self.thesis_service.delete_thesis(
                supervisor=self.supervisor_2,
                thesis_pk=self.thesis_1.pk
            )


    def test_delete_thesis(self):
        self.thesis_service.delete_thesis(
            supervisor=self.supervisor_4,
            thesis_pk=self.thesis_1.pk
        )

        self.assertEqual(Thesis.objects.all().count(), 3)


    def test_get_promotor_theses_invalid_supervisor_id(self):
        with self.assertRaises(InvalidSupervisorIdException):
            self.thesis_service.get_promotor_theses(supervisor=self.non_supervisor)


    def test_get_promotor_theses(self):
        p1_theses = self.thesis_service.get_promotor_theses(supervisor=self.supervisor_1)
        p2_theses = self.thesis_service.get_promotor_theses(supervisor=self.supervisor_2)
        p3_theses = self.thesis_service.get_promotor_theses(supervisor=self.supervisor_3)
        p4_theses = self.thesis_service.get_promotor_theses(supervisor=self.supervisor_4)

        self.assertEqual(p1_theses.count(), 1)
        self.assertEqual(p2_theses.count(), 1)
        self.assertEqual(p3_theses.count(), 1)
        self.assertEqual(p4_theses.count(), 1)
