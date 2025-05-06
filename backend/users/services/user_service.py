from django.db import transaction
from users.models import User, StudentProfile, SupervisorProfile, Role, Logs
from django.utils import timezone
from common.logging_utils import compare_instance_changes
from django.db.models.fields.related_descriptors import ManyToManyDescriptor 


class UserService:
    @transaction.atomic
    def update_user_data(self, user: User, validated_data: dict) -> User:
        try:
            original_user = User.objects.select_related('studentprofile', 'supervisorprofile').get(pk=user.pk)
            original_student_profile = original_user.studentprofile if hasattr(original_user, 'studentprofile') else None
            original_supervisor_profile = original_user.supervisorprofile if hasattr(original_user, 'supervisorprofile') else None
            
            original_user_copy_for_comparison = User.objects.get(pk=user.pk) 

        except User.DoesNotExist:
            raise ValueError(f"User with id {user.pk} doesn't exist.")

        user_data_to_process = validated_data.get('user', {}).copy()
        
        top_level_user_fields_potentially_updateable = ['description', 'first_name', 'last_name', 'email', 'academic_title'] 
        
        for field in top_level_user_fields_potentially_updateable:
             if field in validated_data and field not in user_data_to_process:
                  user_data_to_process[field] = validated_data[field]

        allowed_user_update_fields = ['description'] 

        user_updated = False
        for field, value in user_data_to_process.items():
            if field in allowed_user_update_fields: 
                if hasattr(user, field) and getattr(user, field) != value:
                     setattr(user, field, value)
                     user_updated = True

        profile_updated = False
        if user.role == Role.SUPERVISOR:
            try:
                supervisor_profile = user.supervisorprofile
                limit_fields = ['bacherol_limit', 'engineering_limit', 'master_limit', 'phd_limit']
                profile_data_to_update = {
                    field: validated_data[field]
                    for field in limit_fields
                    if field in validated_data
                }

                if profile_data_to_update:
                    for field, value in profile_data_to_update.items():
                        if hasattr(supervisor_profile, field) and getattr(supervisor_profile, field) != value:
                             setattr(supervisor_profile, field, value)
                             profile_updated = True
                             
                    if profile_updated:
                         supervisor_profile.save()

            except SupervisorProfile.DoesNotExist:
                 print(f"Error in service: Supervisor {user.username} (ID: {user.id}) doesn't have a supervisor profile during limit update!")
                 pass

        if user_updated:
            user.updated_at = timezone.now()
            user.save()

        if user_updated or profile_updated:
             user.refresh_from_db()

        all_changes = []

        user_changes_for_logging = compare_instance_changes(original_user_copy_for_comparison, user, prefix='User')
        all_changes.extend(user_changes_for_logging)

        if user.role == Role.STUDENT and original_student_profile:
            updated_student_profile = user.studentprofile 
            if updated_student_profile:
                 pass

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
                  timestamp=timezone.now(),
            )

        return user

    @transaction.atomic
    def update_user_tags(self, user: User, validated_data: dict):
        tags_to_remove = validated_data.get('to_remove', []) 
        tags_to_add = validated_data.get('to_add', [])       
        
        original_tags_list = list(user.tags.all()) 

        if not tags_to_add and not tags_to_remove:
             return user.tags.all() 
             
        if tags_to_add:
             user.tags.add(*tags_to_add) 

        if tags_to_remove:
             user.tags.remove(*tags_to_remove) 

        user.refresh_from_db() 

        updated_tags_list = list(user.tags.all())

        original_tags_set = set(original_tags_list)
        updated_tags_set = set(updated_tags_list)

        added_tags = updated_tags_set - original_tags_set
        removed_tags = original_tags_set - updated_tags_set

        loggable_changes_descriptions = []

        if added_tags:
            added_tags_names = sorted([tag.name for tag in added_tags])
            loggable_changes_descriptions.append(f'Dodano tagi: {", ".join(added_tags_names)}')

        if removed_tags:
            removed_tags_names = sorted([tag.name for tag in removed_tags])
            loggable_changes_descriptions.append(f'Usunięto tagi: {", ".join(removed_tags_names)}')

        if loggable_changes_descriptions:
            changed_fields_str = f'Użytkownik o ID: {user.id} ({user.username}) zmienił tagi. ' + ' | '.join(loggable_changes_descriptions)

            Logs.objects.create(
                 user_id=user, 
                 description=changed_fields_str,
                 timestamp=timezone.now(),
            )

        return user.tags.all()
        

user_service = UserService()