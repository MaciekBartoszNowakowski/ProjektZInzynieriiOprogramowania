from django.db.models import Model

def compare_instance_changes(old_instance: Model, new_instance: Model, prefix: str = '') -> list:
    changes = []
    if old_instance is None or new_instance is None or old_instance.__class__ != new_instance.__class__:
         return changes

    for field in old_instance._meta.concrete_fields:
        if field.primary_key:
            continue

        old_value = getattr(old_instance, field.name)
        new_value = getattr(new_instance, field.name)

        if field.is_relation and field.many_to_one:
             old_value_id = old_value.pk if old_value else None
             new_value_id = new_value.pk if new_value else None
             if old_value_id != new_value_id:
                  field_name = f'{prefix}.{field.name}_id' if prefix else f'{field.name}_id'
                  changes.append((field_name, old_value_id, new_value_id))
             continue 

        if old_value != new_value:
            field_name = f'{prefix}.{field.name}' if prefix else field.name
            changes.append((field_name, old_value, new_value))

    return changes