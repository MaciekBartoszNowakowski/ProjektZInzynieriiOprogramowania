from django.test import TestCase
from common.models import Department, Tag
from users.models import User, Role, AcademicTitle, StudentProfile, SupervisorProfile
from thesis.models import Thesis, ThesisStatus, ThesisType
from applications.models import Submission, SubmissionStatus
from applications.services.submission_service import *


class TestSubmissionService(TestCase):
    def setUp(self):
        self.department_1 = Department.objects.create(name="Wydział A")
        self.department_2 = Department.objects.create(name="Wydział B")

        tag_python = Tag.objects.create(name="Python")
        tag_ml = Tag.objects.create(name="ML")
        tag_math = Tag.objects.create(name="Math")

        self.supervisor_1 = SupervisorProfile.objects.create(
            user=User.objects.create_user(
                username="supervisor1",
                first_name="Jan",
                last_name="Kowalski",
                academic_title=AcademicTitle.PROFESSOR,
                role=Role.SUPERVISOR,
                department=self.department_1,
            )
        )
        self.supervisor_1.user.tags.add(tag_math, tag_ml)

        self.supervisor_2 = SupervisorProfile.objects.create(
            user=User.objects.create_user(
                username="supervisor2",
                first_name="Anna",
                last_name="Nowak",
                academic_title=AcademicTitle.DOCTOR,
                role=Role.SUPERVISOR,
                department=self.department_2,
            )
        )
        self.supervisor_2.user.tags.add(tag_python, tag_ml)

        self.student_1 = StudentProfile.objects.create(
            user=User.objects.create_user(
                username="student1",
                first_name="Piotr",
                last_name="Student",
                academic_title=AcademicTitle.NONE,
                role=Role.STUDENT,
                department=self.department_1,
            ),
            index_number="123456"
        )

        self.student_2 = StudentProfile.objects.create(
            user=User.objects.create_user(
                username="student2",
                first_name="Maria",
                last_name="Studentka",
                academic_title=AcademicTitle.NONE,
                role=Role.STUDENT,
                department=self.department_1,
            ),
            index_number="123457"
        )

        self.student_3 = StudentProfile.objects.create(
            user=User.objects.create_user(
                username="student3",
                first_name="Adam",
                last_name="Kowalczyk",
                academic_title=AcademicTitle.NONE,
                role=Role.STUDENT,
                department=self.department_2,
            ),
            index_number="123458"
        )

        self.non_student = User.objects.create_user(
            username="coordinator",
            first_name="Tomasz",
            last_name="Koordynator",
            academic_title=AcademicTitle.MASTER,
            role=Role.COORDINATOR,
            department=self.department_1,
        )

        self.thesis_open = Thesis.objects.create(
            supervisor_id=self.supervisor_1,
            thesis_type=ThesisType.ENGINEERING,
            name="Analiza algorytmów sortowania",
            max_students=2,
            status=ThesisStatus.APP_OPEN
        )

        self.thesis_closed = Thesis.objects.create(
            supervisor_id=self.supervisor_1,
            thesis_type=ThesisType.MASTER,
            name="Uczenie maszynowe w praktyce",
            max_students=1,
            status=ThesisStatus.APP_CLOSED
        )

        self.thesis_finished = Thesis.objects.create(
            supervisor_id=self.supervisor_2,
            thesis_type=ThesisType.BACHELOR,
            name="Podstawy programowania",
            max_students=1,
            status=ThesisStatus.FINISHED
        )

        self.thesis_single_student = Thesis.objects.create(
            supervisor_id=self.supervisor_2,
            thesis_type=ThesisType.ENGINEERING,
            name="Praca dla jednego studenta",
            max_students=1,
            status=ThesisStatus.APP_OPEN
        )

        self.submission_service = SubmissionService()


    def test_submit_to_thesis_invalid_student_id(self):
        with self.assertRaises(InvalidStudentIdException):
            self.submission_service.submit_to_thesis(
                student=self.non_student,
                thesis_id=self.thesis_open.id
            )


    def test_submit_to_thesis_invalid_thesis_id(self):
        with self.assertRaises(InvalidThesisIdException):
            self.submission_service.submit_to_thesis(
                student=self.student_1.user,
                thesis_id=999999
            )


    def test_submit_to_thesis_not_available(self):
        with self.assertRaises(ThesisNotAvailableException):
            self.submission_service.submit_to_thesis(
                student=self.student_1.user,
                thesis_id=self.thesis_closed.id
            )


    def test_submit_to_thesis_not_available_finished(self):
        with self.assertRaises(ThesisNotAvailableException):
            self.submission_service.submit_to_thesis(
                student=self.student_1.user,
                thesis_id=self.thesis_finished.id
            )


    def test_submit_to_thesis_student_already_assigned(self):
        Submission.objects.create(
            student=self.student_1,
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        with self.assertRaises(StudentAlreadyAssignedException):
            self.submission_service.submit_to_thesis(
                student=self.student_1.user,
                thesis_id=self.thesis_single_student.id
            )


    def test_submit_to_thesis_success(self):
        submission = self.submission_service.submit_to_thesis(
            student=self.student_1.user,
            thesis_id=self.thesis_open.id
        )

        self.assertIsNotNone(submission)
        self.assertEqual(submission.student, self.student_1)
        self.assertEqual(submission.thesis, self.thesis_open)
        self.assertEqual(Submission.objects.count(), 1)


    def test_cancel_submission_invalid_student_id(self):
        with self.assertRaises(InvalidStudentIdException):
            self.submission_service.cancel_submission(student=self.non_student)


    def test_cancel_submission_no_submission(self):
        with self.assertRaises(ValueError):
            self.submission_service.cancel_submission(student=self.student_1.user)


    def test_cancel_submission_already_accepted(self):
        Submission.objects.create(
            student=self.student_1,
            thesis=self.thesis_open,
            status=SubmissionStatus.ACCEPTED
        )

        with self.assertRaises(SubmissionAlreadyResolvedException):
            self.submission_service.cancel_submission(student=self.student_1.user)


    def test_cancel_submission_already_rejected(self):
        Submission.objects.create(
            student=self.student_1,
            thesis=self.thesis_open,
            status=SubmissionStatus.REJECTED
        )

        with self.assertRaises(SubmissionAlreadyResolvedException):
            self.submission_service.cancel_submission(student=self.student_1.user)


    def test_cancel_submission_success(self):
        Submission.objects.create(
            student=self.student_1,
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        result = self.submission_service.cancel_submission(student=self.student_1.user)

        self.assertIn("message", result)
        self.assertEqual(Submission.objects.count(), 0)


    def test_get_student_submission_invalid_student_id(self):
        with self.assertRaises(InvalidStudentIdException):
            self.submission_service.get_student_submission(student=self.non_student)


    def test_get_student_submission_no_submission(self):
        result = self.submission_service.get_student_submission(student=self.student_1.user)
        self.assertIsNone(result)


    def test_get_student_submission_success(self):
        submission = Submission.objects.create(
            student=self.student_1,
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        result = self.submission_service.get_student_submission(student=self.student_1.user)
        self.assertEqual(result, submission)


    def test_get_thesis_with_submissions_invalid_supervisor_id(self):
        with self.assertRaises(InvalidSupervisorIdException):
            self.submission_service.get_thesis_with_submissions(
                supervisor=self.non_student,
                thesis_id=self.thesis_open.id
            )


    def test_get_thesis_with_submissions_invalid_thesis_id(self):
        with self.assertRaises(InvalidThesisIdException):
            self.submission_service.get_thesis_with_submissions(
                supervisor=self.supervisor_1.user,
                thesis_id=999999
            )


    def test_get_thesis_with_submissions_wrong_supervisor(self):
        with self.assertRaises(InvalidThesisIdException):
            self.submission_service.get_thesis_with_submissions(
                supervisor=self.supervisor_2.user,
                thesis_id=self.thesis_open.id
            )


    def test_get_thesis_with_submissions_success(self):
        Submission.objects.create(
            student=self.student_1, 
            thesis=self.thesis_open, 
            status=SubmissionStatus.OPEN
        )

        Submission.objects.create(
            student=self.student_2, 
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        Submission.objects.create(
            student=self.student_3, 
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        thesis = self.submission_service.get_thesis_with_submissions(
            supervisor=self.supervisor_1.user,
            thesis_id=self.thesis_open.id
        )

        self.assertEqual(thesis, self.thesis_open)
        self.assertEqual(thesis.submission_set.count(), 3)


    def test_accept_submission_invalid_supervisor_id(self):
        submission = Submission.objects.create(
            student=self.student_1, 
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        with self.assertRaises(InvalidSupervisorIdException):
            self.submission_service.accept_submission(
                supervisor=self.non_student,
                submission_id=submission.id
            )


    def test_accept_submission_invalid_submission_id(self):
        with self.assertRaises(ValueError):
            self.submission_service.accept_submission(
                supervisor=self.supervisor_1.user,
                submission_id=999999
            )


    def test_accept_submission_wrong_supervisor(self):
        submission = Submission.objects.create(
            student=self.student_1, 
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        with self.assertRaises(ValueError):
            self.submission_service.accept_submission(
                supervisor=self.supervisor_2.user,
                submission_id=submission.id
            )


    def test_accept_submission_already_accepted(self):
        submission = Submission.objects.create(
            student=self.student_1, 
            thesis=self.thesis_open,
            status=SubmissionStatus.ACCEPTED
        )

        with self.assertRaises(SubmissionAlreadyResolvedException):
            self.submission_service.accept_submission(
                supervisor=self.supervisor_1.user,
                submission_id=submission.id
            )


    def test_accept_submission_already_rejected(self):
        submission = Submission.objects.create(
            student=self.student_1, 
            thesis=self.thesis_open,
            status=SubmissionStatus.REJECTED
        )

        with self.assertRaises(SubmissionAlreadyResolvedException):
            self.submission_service.accept_submission(
                supervisor=self.supervisor_1.user,
                submission_id=submission.id
            )


    def test_accept_submission_thesis_full(self):
        submission1 = Submission.objects.create(
            student=self.student_1,
            thesis=self.thesis_single_student,
            status=SubmissionStatus.OPEN
        )

        submission2 = Submission.objects.create(
            student=self.student_3,
            thesis=self.thesis_single_student,
            status=SubmissionStatus.OPEN
        )

        self.submission_service.accept_submission(
            supervisor=self.supervisor_2.user,
            submission_id=submission1.id
        )

        with self.assertRaises(ThesisFullException):
            self.submission_service.accept_submission(
                supervisor=self.supervisor_2.user,
                submission_id=submission2.id
            )


    def test_accept_submission_success(self):
        submission1 = Submission.objects.create(
            student=self.student_2, 
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        submission2 = Submission.objects.create(
            student=self.student_3, 
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        result = self.submission_service.accept_submission(
            supervisor=self.supervisor_1.user,
            submission_id=submission1.id
        )

        self.assertEqual(result, submission1)
        self.thesis_open.refresh_from_db()
        self.assertEqual(self.thesis_open.status, ThesisStatus.APP_OPEN)

        result = self.submission_service.accept_submission(
            supervisor=self.supervisor_1.user,
            submission_id=submission2.id
        )

        self.assertEqual(result, submission2)
        self.thesis_open.refresh_from_db()
        self.assertEqual(self.thesis_open.status, ThesisStatus.APP_CLOSED)

        self.assertEqual(Submission.objects.count(), 2)
        submission1.refresh_from_db()
        self.assertEqual(submission1.status, SubmissionStatus.ACCEPTED)
        submission2.refresh_from_db()
        self.assertEqual(submission2.status, SubmissionStatus.ACCEPTED)


    def test_reject_submission_invalid_supervisor_id(self):
        submission = Submission.objects.create(
            student=self.student_1, 
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        with self.assertRaises(InvalidSupervisorIdException):
            self.submission_service.reject_submission(
                supervisor=self.non_student,
                submission_id=submission.id
            )


    def test_reject_submission_invalid_submission_id(self):
        with self.assertRaises(ValueError):
            self.submission_service.reject_submission(
                supervisor=self.supervisor_1.user,
                submission_id=999999
            )


    def test_reject_submission_already_accepted(self):
        submission = Submission.objects.create(
            student=self.student_1, 
            thesis=self.thesis_open,
            status=SubmissionStatus.ACCEPTED
        )

        with self.assertRaises(SubmissionAlreadyResolvedException):
            self.submission_service.accept_submission(
                supervisor=self.supervisor_1.user,
                submission_id=submission.id
            )


    def test_reject_submission_already_rejected(self):
        submission = Submission.objects.create(
            student=self.student_1, 
            thesis=self.thesis_open,
            status=SubmissionStatus.REJECTED
        )

        with self.assertRaises(SubmissionAlreadyResolvedException):
            self.submission_service.accept_submission(
                supervisor=self.supervisor_1.user,
                submission_id=submission.id
            )


    def test_reject_submission_success(self):
        submission = Submission.objects.create(
            student=self.student_1, 
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        result = self.submission_service.reject_submission(
            supervisor=self.supervisor_1.user,
            submission_id=submission.id
        )

        self.assertIn("message", result)
        self.assertEqual(Submission.objects.count(), 1)
        submission.refresh_from_db()
        self.assertEqual(submission.status, SubmissionStatus.REJECTED)


    def test_remove_student_from_thesis_invalid_supervisor_id(self):
        submission = Submission.objects.create(
            student=self.student_1, 
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        with self.assertRaises(InvalidSupervisorIdException):
            self.submission_service.remove_student_from_thesis(
                supervisor=self.non_student,
                submission_id=submission.id
            )


    def test_remove_student_from_thesis_invalid_submission_id(self):
        with self.assertRaises(ValueError):
            self.submission_service.remove_student_from_thesis(
                supervisor=self.supervisor_1.user,
                submission_id=999999
            )


    def test_remove_student_from_thesis_wrong_supervisor(self):
        submission = Submission.objects.create(
            student=self.student_1, 
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        with self.assertRaises(ValueError):
            self.submission_service.remove_student_from_thesis(
                supervisor=self.supervisor_2.user,
                submission_id=submission.id
            )


    def test_remove_not_accepted_submission(self):
        submission = Submission.objects.create(
            student=self.student_2, 
            thesis=self.thesis_single_student,
            status=SubmissionStatus.OPEN
        )

        with self.assertRaises(SubmissionNotAcceptedException):
            self.submission_service.remove_student_from_thesis(
                supervisor=self.supervisor_2.user,
                submission_id=submission.id
            )


    def test_remove_student_reopens_closed_thesis(self):
        submission = Submission.objects.create(
            student=self.student_3, 
            thesis=self.thesis_single_student,
            status=SubmissionStatus.OPEN
        )
        
        self.submission_service.accept_submission(
            supervisor=self.supervisor_2.user,
            submission_id=submission.id
        )

        self.thesis_single_student.refresh_from_db()
        self.assertEqual(self.thesis_single_student.status, ThesisStatus.APP_CLOSED)
        self.assertEqual(Submission.objects.count(), 1)

        self.submission_service.remove_student_from_thesis(
            supervisor=self.supervisor_2.user,
            submission_id=submission.id
        )

        self.thesis_single_student.refresh_from_db()
        self.assertEqual(self.thesis_single_student.status, ThesisStatus.APP_OPEN)
        self.assertEqual(Submission.objects.count(), 0)


    def test_remove_student_from_thesis_success(self):
        submission = Submission.objects.create(
            student=self.student_1, 
            thesis=self.thesis_open,
            status=SubmissionStatus.OPEN
        )

        self.submission_service.accept_submission(
            supervisor=self.supervisor_1.user,
            submission_id=submission.id
        )

        result = self.submission_service.remove_student_from_thesis(
            supervisor=self.supervisor_1.user,
            submission_id=submission.id
        )

        self.assertIn("message", result)
        self.assertEqual(Submission.objects.count(), 0)
