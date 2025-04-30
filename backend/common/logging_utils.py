def get_changed_fields(id, this, other):
    if not isinstance(other, this.__class__):
        return None
    
    changed_fields = []
        
    for field in this._meta.concrete_fields:
        self_value = getattr(this, field.name)
        other_value = getattr(other, field.name)
            
        if self_value != other_value:
            changed_fields.append((field.name, other_value, self_value))

    if len(changed_fields) == 0:
        return None
    
    changed_fields_str = f'Użytkownik o ID: {id} zmienił pola: ' + ','.join(
        [f'{name}: z {old} na {new}' for name, old, new in changed_fields])
    
    return changed_fields_str