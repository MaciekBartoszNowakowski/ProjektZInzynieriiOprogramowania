from django.utils import timezone
from applications.models import Submission, SubmissionStatus
from thesis.models import Thesis, ThesisStatus
from users.models import StudentProfile, SupervisorProfile, User, Logs


class InvalidStudentIdException(ValueError):
    pass


class InvalidThesisIdException(ValueError):
    pass


class InvalidSupervisorIdException(ValueError):
    pass


class ThesisNotAvailableException(ValueError):
    pass


class StudentAlreadyAssignedException(ValueError):
    pass


class ThesisFullException(ValueError):
    pass


class SubmissionAlreadyResolvedException(ValueError):
    pass


class SubmissionNotAcceptedException(ValueError):
    pass


class SubmissionService:
    def submit_to_thesis(self, student: User, thesis_id: int):
        try:
            student_profile = StudentProfile.objects.get(pk=student.pk)
        except StudentProfile.DoesNotExist:
            raise InvalidStudentIdException(f"Nie znaleziono studenta o id: {student.pk}")
        
        try:
            thesis = Thesis.objects.get(pk=thesis_id)
        except Thesis.DoesNotExist:
            raise InvalidThesisIdException(f"Nie znaleziono pracy o id: {thesis_id}")
        
        if thesis.status != ThesisStatus.APP_OPEN:
            raise ThesisNotAvailableException(f"Praca o id {thesis_id} nie jest dostępna do zapisów. Status: {thesis.status}")
        
        if Submission.objects.filter(student=student_profile).exists():
            existing_submission = Submission.objects.get(student=student_profile)
            raise StudentAlreadyAssignedException(
                f"Student jest już zapisany na pracę: {existing_submission.thesis.name} (ID: {existing_submission.thesis.id})"
            )
        
        submission = Submission.objects.create(
            student=student_profile,
            thesis=thesis,
            status=SubmissionStatus.OPEN
        )
        
        log_description = f"""Student o ID {student.pk} ({student_profile.index_number}) 
zapisał się na pracę dyplomową '{thesis.name}' (ID: {thesis.id}) 
prowadzoną przez {thesis.supervisor_id.user.get_full_name()}"""
        
        Logs.objects.create(
            user_id=student,
            description=log_description,
            timestamp=timezone.now(),
        )
        
        return submission
    

    def cancel_submission(self, student: User):
        try:
            student_profile = StudentProfile.objects.get(pk=student.pk)
        except StudentProfile.DoesNotExist:
            raise InvalidStudentIdException(f"Nie znaleziono studenta o id: {student.pk}")
        
        try:
            submission = Submission.objects.get(student=student_profile)
        except Submission.DoesNotExist:
            raise ValueError("Student nie jest zapisany na żadną pracę")
        
        if submission.status != SubmissionStatus.OPEN:
            raise SubmissionAlreadyResolvedException(f"Nie można anulować tego zgłoszenia, bo nie jest aktywne! Stan zgłoszenia: {submission.status}")
        
        thesis = submission.thesis
        thesis_name = thesis.name
        thesis_id = thesis.id
        
        submission.delete()
        
        log_description = f"""Student o ID {student.pk} ({student_profile.index_number}) 
anulował zgłoszenie na pracę '{thesis_name}' (ID: {thesis_id})"""
        
        Logs.objects.create(
            user_id=student,
            description=log_description,
            timestamp=timezone.now(),
        )
        
        return {"message": f"Anulowano zgłoszenie na pracę '{thesis_name}'"}
    

    def get_student_submission(self, student: User):
        try:
            student_profile = StudentProfile.objects.get(pk=student.pk)
            submission = Submission.objects.select_related('thesis', 'thesis__supervisor_id__user').get(student=student_profile)
            return submission
        except StudentProfile.DoesNotExist:
            raise InvalidStudentIdException(f"Nie znaleziono studenta o id: {student.pk}")
        except Submission.DoesNotExist:
            return None

     
    def get_thesis_with_submissions(self, supervisor: User, thesis_id: int):
        try:
            supervisor_profile = SupervisorProfile.objects.get(pk=supervisor.pk)
        except SupervisorProfile.DoesNotExist:
            raise InvalidSupervisorIdException(f"Nie znaleziono promotora o id: {supervisor.pk}")
        
        try:
            thesis = Thesis.objects.prefetch_related('submission_set__student__user').get(
                pk=thesis_id, 
                supervisor_id=supervisor_profile
            )
            return thesis
        except Thesis.DoesNotExist:
            raise InvalidThesisIdException(f"Nie znaleziono pracy o id: {thesis_id} prowadzonej przez promotora o id: {supervisor.pk}")


    def accept_submission(self, supervisor: User, submission_id: int):
        try:
            supervisor_profile = SupervisorProfile.objects.get(pk=supervisor.pk)
        except SupervisorProfile.DoesNotExist:
            raise InvalidSupervisorIdException(f"Nie znaleziono promotora o id: {supervisor.pk}")
        
        try:
            submission = Submission.objects.select_related('thesis', 'student__user').get(
                pk=submission_id, 
                thesis__supervisor_id=supervisor_profile
            )
        except Submission.DoesNotExist:
            raise ValueError(f"Nie znaleziono zgłoszenia o id: {submission_id} dla tego promotora")
        
        if submission.status != SubmissionStatus.OPEN:
            raise SubmissionAlreadyResolvedException(f"Nie można zaakceptować tego zgłoszenia, bo nie jest aktywne! Stan zgłoszenia: {submission.status}")

        thesis = submission.thesis
        accepted_students = Submission.objects.filter(
            thesis=thesis, 
            status=SubmissionStatus.ACCEPTED
        ).count()

        if accepted_students >= thesis.max_students:
            raise ThesisFullException(f"Praca '{thesis.name}' osiągnęła maksymalną liczbę studentów ({thesis.max_students})")
        
        submission.status = SubmissionStatus.ACCEPTED
        submission.save()

        if accepted_students == thesis.max_students - 1: # last student has just been accepted
            thesis.status = ThesisStatus.APP_CLOSED
            thesis.updated_at = timezone.now()
            thesis.save()
                
        log_description = f"Promotor o ID {supervisor.pk} zaakceptował zgłoszenie studenta {submission.student.user.get_full_name()} (ID: {submission.student.pk}) na pracę '{thesis.name}' (ID: {thesis.id})"
        
        Logs.objects.create(
            user_id=supervisor,
            description=log_description,
            timestamp=timezone.now(),
        )
        
        return submission


    def reject_submission(self, supervisor: User, submission_id: int):
        try:
            supervisor_profile = SupervisorProfile.objects.get(pk=supervisor.pk)
        except SupervisorProfile.DoesNotExist:
            raise InvalidSupervisorIdException(f"Nie znaleziono promotora o id: {supervisor.pk}")
        
        try:
            submission = Submission.objects.select_related('thesis', 'student__user').get(
                pk=submission_id, 
                thesis__supervisor_id=supervisor_profile
            )
        except Submission.DoesNotExist:
            raise ValueError(f"Nie znaleziono zgłoszenia o id: {submission_id} dla tego promotora")
        
        if submission.status != SubmissionStatus.OPEN:
            raise SubmissionAlreadyResolvedException(f"Nie można odrzucić tego zgłoszenia, bo nie jest aktywne! Stan zgłoszenia: {submission.status}")

        thesis = submission.thesis
        student_name = submission.student.user.get_full_name()
        student_id = submission.student.pk
        submission.status = SubmissionStatus.REJECTED
        submission.save()
        
        log_description = f"Promotor o ID {supervisor.pk} odrzucił zgłoszenie studenta {student_name} (ID: {student_id}) na pracę '{thesis.name}' (ID: {thesis.id})"
        
        Logs.objects.create(
            user_id=supervisor,
            description=log_description,
            timestamp=timezone.now(),
        )
        
        return {"message": f"Odrzucono zgłoszenie studenta {student_name}"}


    def remove_student_from_thesis(self, supervisor: User, submission_id: int):
        try:
            supervisor_profile = SupervisorProfile.objects.get(pk=supervisor.pk)
        except SupervisorProfile.DoesNotExist:
            raise InvalidSupervisorIdException(f"Nie znaleziono promotora o id: {supervisor.pk}")
        
        try:
            submission = Submission.objects.select_related('thesis', 'student__user').get(
                pk=submission_id, 
                thesis__supervisor_id=supervisor_profile
            )
        except Submission.DoesNotExist:
            raise ValueError(f"Nie znaleziono zgłoszenia o id: {submission_id} dla tego promotora")
        
        if submission.status != SubmissionStatus.ACCEPTED:
            raise SubmissionNotAcceptedException(f"Nie można usunąć niezaakceptowanego zgłoszenia! Stan zgłoszenia: {submission.status}")

        thesis = submission.thesis
        student_name = submission.student.user.get_full_name()
        student_id = submission.student.pk
        
        submission.delete()
        
        remaining_accepted_submissions = Submission.objects.filter(
            thesis=thesis,
            status=SubmissionStatus.ACCEPTED
        ).count()

        if remaining_accepted_submissions < thesis.max_students and thesis.status == ThesisStatus.APP_CLOSED:
            thesis.status = ThesisStatus.APP_OPEN
            thesis.updated_at = timezone.now()
            thesis.save()
        
        log_description = f"Promotor o ID {supervisor.pk} usunął studenta {student_name} (ID: {student_id}) z pracy '{thesis.name}' (ID: {thesis.id})"
        
        Logs.objects.create(
            user_id=supervisor,
            description=log_description,
            timestamp=timezone.now(),
        )
        
        return {"message": f"Usunięto studenta {student_name} z pracy"}
