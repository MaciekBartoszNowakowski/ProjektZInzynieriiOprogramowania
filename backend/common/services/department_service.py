from django.db import transaction
from users.models import Logs, User
from common.models import Department
from django.utils import timezone
from common.logging_utils import compare_instance_changes
from common.serializers.department_serializer import DepartmentSerializer


class DepartmentService:
    @transaction.atomic
    def update_department(self, coordinator: User, validated_data: dict) -> Department:
        department = coordinator.department
        
        new_name = validated_data.get('name', '')
        new_description = validated_data.get('description', '')

        
        changes = ''
        if new_name != '' and new_name != department.name:
            changes += f'zmienił nazwę wydziału z {department.name} na {new_name}'
            department.name = new_name
            
        if new_description != '' and new_description != department.description:
            changes += f'zmienił opis wydziału z {department.description} na {new_description}'
            department.description = new_description
            
        department.save()
        
        if changes != '':
            changes = f'Koordynator o ID {coordinator.id} dokonał następujących zmian: ' + changes
            
            Logs.objects.create(
                user_id=coordinator, 
                description=changes,
                timestamp=timezone.now(),
            )
            
        return department
        
department_service = DepartmentService()