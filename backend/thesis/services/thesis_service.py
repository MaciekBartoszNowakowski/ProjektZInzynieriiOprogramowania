from django.utils import timezone
from thesis.models import Thesis, ThesisStatus, ThesisType
from users.models import User, SupervisorProfile, Logs, ACADEMIC_TITLE_SORT_ORDER, AcademicTitle
from common.models import Tag
from thesis.serializers.thesis_delete_serializer import ThesisDeleteSerializer


class InvalidSupervisorIdException(ValueError):
    pass


class InvalidThesisTypeException(ValueError):
    pass


class SupervisorTitleRequiredException(ValueError):
    pass


class ThesisTypeLimitExceededException(Exception):
    pass


class NonPositiveStudentsLimitException(ValueError):
    pass


class InvalidThesisIdException(ValueError):
    pass


class InvalidThesisStatusException(ValueError):
    pass


class ThesisService:
    def __init__(self):
        self.type_limits_dict = {
            ThesisType.BACHELOR: "bacherol_limit",
            ThesisType.ENGINEERING: "engineering_limit",
            ThesisType.MASTER: "master_limit",
            ThesisType.DOCTOR: "phd_limit"
        }

    def add_new_thesis(
        self,
        supervisor: User,
        validated_data: dict
    ):
        try:
            supervisor = SupervisorProfile.objects.get(pk=supervisor.pk)
        except SupervisorProfile.DoesNotExist:
            raise InvalidSupervisorIdException(f"Nie znaleziono promotora o id: {supervisor.pk}")

        thesis_type = validated_data.get('thesis_type')
        name = validated_data.get('name')
        description = validated_data.get('description')
        max_students = validated_data.get('max_students', 1) 
        language = validated_data.get('language', "English")
        tags = validated_data.get('tags', set())

        if thesis_type not in self.type_limits_dict:
            raise InvalidThesisTypeException(f"Błędny typ pracy: {thesis_type}")
        
        academic_titles_to_add_thesis = {
            ThesisType.BACHELOR: AcademicTitle.MASTER,
            ThesisType.ENGINEERING: AcademicTitle.MASTER,
            ThesisType.MASTER: AcademicTitle.DOCTOR,
            ThesisType.DOCTOR: AcademicTitle.HABILITATED_DOCTOR
        }

        supervisor_title = supervisor.user.academic_title
        required_title = academic_titles_to_add_thesis[thesis_type]
        if ACADEMIC_TITLE_SORT_ORDER[supervisor_title] < ACADEMIC_TITLE_SORT_ORDER[required_title]:
            raise SupervisorTitleRequiredException(
                f"Ten promotor nie ma wymaganego tytułu: {required_title}, który trzeba mieć, aby dodać pracę: {thesis_type}. Tytuł naukowy promotora: {supervisor_title}."
            )
    
        limit_left = getattr(supervisor, self.type_limits_dict[thesis_type])
        if limit_left <= 0:
            raise ThesisTypeLimitExceededException(
                f"Ten promotor wyczerpał już swój limit na pracę: {thesis_type}"
            )
        
        if max_students < 1:
            raise NonPositiveStudentsLimitException(f"Liczba studentów na pracę powinna być dodatnia. Otrzymano {max_students}")
        
        for tag in tags:
            if not isinstance(tag, Tag):
                raise TypeError(f"Błędny typ tagu {tag}: {type(tag)}, powinien być: <class 'common.models.Tag'>")

        setattr(supervisor, self.type_limits_dict[thesis_type], limit_left - 1)
        supervisor.save()

        added_thesis = Thesis.objects.create(
            supervisor_id=supervisor,
            thesis_type=thesis_type,
            name=name,
            description=description,
            max_students=max_students,
            status=ThesisStatus.APP_OPEN,
            language=language
        )
        added_thesis.tags.set(tags)

        log_description = f"""Promotor o ID {supervisor.pk} dodał
nową pracę dyplomową (rodzaj: {thesis_type}) o ID {added_thesis.pk}"""

        Logs.objects.create(
            user_id=supervisor.user,
            description=log_description,
            timestamp=timezone.now(),
        )

    def update_thesis(
        self,
        supervisor: User,
        thesis_pk: int,
        validated_data: dict
    ):
        try:
            supervisor = SupervisorProfile.objects.get(pk=supervisor.pk)
        except SupervisorProfile.DoesNotExist:
            raise InvalidSupervisorIdException(f"Nie znaleziono promotora o id: {supervisor.pk}")
        
        try:
            thesis_to_update = Thesis.objects.get(pk=thesis_pk, supervisor_id=supervisor)
        except Thesis.DoesNotExist:
            raise InvalidThesisIdException(f"Nie znaleziono pracy o id: {thesis_pk} prowadzonej przez promotora o id: {supervisor.pk}")
        
        tags = validated_data.get("tags", set())
        for tag in tags:
            if not isinstance(tag, Tag):
                raise TypeError(f"Błędny typ tagu {tag}: {type(tag)}, powinien być: <class 'common.models.Tag'>")

        updated = False
        changes_dict = {}

        for attribute in validated_data:
            old_value = getattr(thesis_to_update, attribute)
            new_value = validated_data[attribute]

            if attribute == "tags":
                if new_value is None: new_value = []
                thesis_to_update.tags.set(new_value)
                
                if new_value != old_value:
                    updated = True
                    changes_dict[attribute] = (old_value, new_value)
            elif new_value not in [None, ""] and new_value != old_value:
                updated = True
                changes_dict[attribute] = (old_value, new_value)
                setattr(thesis_to_update, attribute, new_value)

        status = validated_data.get("status")
        if status not in [
            ThesisStatus.APP_OPEN,
            ThesisStatus.APP_CLOSED,
            ThesisStatus.FINISHED
        ]:
            raise InvalidThesisStatusException(f"Błędny status pracy: {status}")

        max_students = validated_data.get("max_students")
        if max_students is not None and max_students < 1:
            raise NonPositiveStudentsLimitException(f"Liczba studentów na pracę powinna być dodatnia. Otrzymano {max_students}")

        if updated:
            thesis_to_update.updated_at = timezone.now()
            thesis_to_update.save()

            log_description = f"""Promotor o ID {supervisor.pk} zmienił
pola w pracy dyplomowej o ID {thesis_to_update.pk}: """
            for attribute in changes_dict:
                old, new = changes_dict[attribute]
                log_description += f"{attribute} z '{old}' na '{new}', "

            log_description = log_description[:-2]
            max_log_desc_length = 500
            if len(log_description) > max_log_desc_length:
                log_description = log_description[:max_log_desc_length - 3] + '...'

            Logs.objects.create(
                user_id=supervisor.user,
                description=log_description,
                timestamp=timezone.now(),
            )
        
        return thesis_to_update
    
    def delete_thesis(
        self,
        supervisor: User,
        thesis_pk: int
    ):
        try:
            supervisor = SupervisorProfile.objects.get(pk=supervisor.pk)
            thesis_to_delete = Thesis.objects.get(pk=thesis_pk, supervisor_id=supervisor)
            serialized_thesis_data = ThesisDeleteSerializer(thesis_to_delete).data
            Thesis.objects.get(pk=thesis_pk, supervisor_id=supervisor).delete()

            thesis_type = thesis_to_delete.thesis_type
            limit_before = getattr(supervisor, self.type_limits_dict[thesis_type])
            setattr(supervisor, self.type_limits_dict[thesis_type], limit_before + 1)
            supervisor.save()

            log_description = f"""Promotor o ID {supervisor.pk} usunął
pracę dyplomową (rodzaj: {thesis_type}) o ID {thesis_to_delete.pk}"""

            Logs.objects.create(
                user_id=supervisor.user,
                description=log_description,
                timestamp=timezone.now(),
            )

            return serialized_thesis_data
        except SupervisorProfile.DoesNotExist:
            raise InvalidSupervisorIdException(f"Nie znaleziono promotora o id: {supervisor.pk}")
        except Thesis.DoesNotExist:
            raise InvalidThesisIdException(f"Nie znaleziono pracy o id: {thesis_pk} prowadzonej przez promotora o id: {supervisor.pk}")
        
    def get_promotor_theses(
        self,
        supervisor: User
    ):
        try:
            supervisor = SupervisorProfile.objects.get(pk=supervisor.pk)
            promotor_theses = Thesis.objects.filter(supervisor_id=supervisor)
            return promotor_theses
        except SupervisorProfile.DoesNotExist:
            raise InvalidSupervisorIdException(f"Nie znaleziono promotora o id: {supervisor.pk}")
 