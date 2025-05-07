from django.core.exceptions import EmptyResultSet
from thesis.models import Thesis, ThesisStatus, ThesisType
from users.models import SupervisorProfile


class InvalidSupervisorIdException(ValueError):
    pass


class InvalidThesisTypeException(ValueError):
    pass


class ThesisTypeLimitExceededException(Exception):
    pass


class NoAvailableThesesException(Exception):
    pass


class NonPositiveStudentsLimitException(ValueError):
    pass


class ThesisService:
    def add_new_thesis(
        self,
        supervisor_id,
        thesis_type: ThesisType,
        name,
        description = None,
        max_students = 1,
        language = "English"
    ):
        try:
            supervisor = SupervisorProfile.objects.get(pk=supervisor_id)
        except EmptyResultSet:
            raise InvalidSupervisorIdException("Niewłaściwy identyfikator promotora!")

        type_limits_dict = {
            ThesisType.BACHELOR: "bacherol_limit",
            ThesisType.ENGINEERING: "engineering_limit",
            ThesisType.MASTER: "master_limit",
            ThesisType.DOCTOR: "phd_limit"
        }

        if thesis_type not in type_limits_dict:
            raise InvalidThesisTypeException(f"Błędny typ pracy: {thesis_type}")
    
        limit_left = getattr(supervisor, type_limits_dict[thesis_type])
        if limit_left <= 0:
            raise ThesisTypeLimitExceededException(
                f"Ten promotor wyczerpał już swój limit na pracę: {thesis_type}"
            )
        
        if max_students < 1:
            raise NonPositiveStudentsLimitException(f"Liczba studentów na pracę powinna być dodatnia. Otrzymano {max_students}")
        
        setattr(supervisor, type_limits_dict[thesis_type], limit_left - 1)
        thesis = Thesis.objects.create(
            supervisor_id=supervisor_id,
            thesis_type=thesis_type,
            name=name,
            description=description,
            max_students=max_students,
            status=ThesisStatus.APP_OPEN,
            language=language
        )
        return thesis
    
    def get_available_theses(self):
        try:
            theses = Thesis.objects.all()
            theses = theses.filter(status=ThesisStatus.APP_OPEN)
        except EmptyResultSet:
            raise NoAvailableThesesException("Nie znaleziono żadnych otwartych prac!")

        return theses
        