from django.db import transaction
from users.models import User, StudentProfile, SupervisorProfile, Role, Logs
from django.utils import timezone
from common.logging_utils import compare_instance_changes

class UserService:
    @transaction.atomic
    def update_user_data(self, user: User, validated_data: dict) -> User:
        try:
            original_user = User.objects.select_related('studentprofile', 'supervisorprofile').get(pk=user.pk)
        except User.DoesNotExist:
            raise ValueError(f"User with id {user.pk} doesn't exist.")

        original_student_profile = original_user.studentprofile if hasattr(original_user, 'studentprofile') else None
        original_supervisor_profile = original_user.supervisorprofile if hasattr(original_user, 'supervisorprofile') else None
        original_user_copy = User.objects.get(pk=user.pk)

        user_fields_data = validated_data.get('user')

        if isinstance(user_fields_data, dict):
            pass
        else:
            user_fields_data = validated_data

        if user_fields_data:
            if 'description' in user_fields_data:
                user.description = user_fields_data.get('description')

        if user.role == Role.STUDENT:
            try:
                student_profile = user.studentprofile
            except StudentProfile.DoesNotExist:
                 pass

        elif user.role == Role.SUPERVISOR:
            try:
                supervisor_profile = user.supervisorprofile
                limit_fields = ['bacherol_limit', 'engineering_limit', 'master_limit', 'phd_limit']
                profile_data_to_update = {
                    field: validated_data[field]
                    for field in limit_fields
                    if field in validated_data
                }

                for field, value in profile_data_to_update.items():
                    setattr(supervisor_profile, field, value)

                if profile_data_to_update:
                    supervisor_profile.save()

            except SupervisorProfile.DoesNotExist:
                print(f"Error in service: Supervisor {user.username} (ID: {user.id}) doesn't have a supervisor profile during limit update!")
                pass

        user_changes = compare_instance_changes(original_user_copy, user, prefix='User')
        if user_changes:
             user.updated_at = timezone.now()
             user.save()

        all_changes = []

        user_changes_for_logging = compare_instance_changes(original_user_copy, user, prefix='User')
        all_changes.extend(user_changes_for_logging)

        if user.role == Role.STUDENT and original_student_profile:
             updated_student_profile = user.studentprofile
             if updated_student_profile:
                 profile_changes_for_logging = compare_instance_changes(original_student_profile, updated_student_profile, prefix='StudentProfile')
                 all_changes.extend(profile_changes_for_logging)

        if user.role == Role.SUPERVISOR and original_supervisor_profile:
             updated_supervisor_profile = user.supervisorprofile
             if updated_supervisor_profile:
                 profile_changes_for_logging = compare_instance_changes(original_supervisor_profile, updated_supervisor_profile, prefix='SupervisorProfile')
                 all_changes.extend(profile_changes_for_logging)

        loggable_changes = [change for change in all_changes if change[0] != 'User.updated_at']

        if loggable_changes:
            changed_fields_str = f'Użytkownik o ID: {user.id} ({user.username}) zmienił pola: ' + ', '.join(
                [f'{name}: z "{str(old)}" na "{str(new)}"' for name, old, new in loggable_changes])

            max_log_desc_length = 500
            if len(changed_fields_str) > max_log_desc_length:
                changed_fields_str = changed_fields_str[:max_log_desc_length - 3] + '...'

            Logs.objects.create(
                user_id=user,
                description=changed_fields_str,
            )

        return user


user_service = UserService()