import random
import string

from django.db import transaction, IntegrityError 
from django.utils import timezone
from django.conf import settings 
from django.core.mail import send_mail

from django.contrib.auth import get_user_model 
from users.models import StudentProfile, SupervisorProfile, Role, AcademicTitle, Logs, User
from common.models import Department 

class AccountCreationService:
    def clean_polish_chars(self, text: str) -> str:
        replacements = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
            'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
            'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def generate_username_from_names(self, first_name: str, last_name: str) -> str:
        base = f"{self.clean_polish_chars(first_name).lower()}{self.clean_polish_chars(last_name).lower()}"
        base = base.replace('-', '').replace(' ', '').replace("'", "") 
        return base[:150] 

    def generate_temporary_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation 
        while True:
            password = ''.join(random.choice(characters) for i in range(length))
            if (any(c.islower() for c in password) and
                any(c.isupper() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in string.punctuation for c in password)):
                break 
        return password

    def send_welcome_email(self, user_email: str, username: str, temporary_password: str):
        subject = 'Twoje konto w systemie - Dane do logowania' 
        message = f"""Witaj,

Twoje konto w systemie dyplom.agh zostało utworzone. Poniżej znajdziesz dane do logowania:

Nazwa użytkownika: {username}
Tymczasowe hasło: {temporary_password}

Ze względów bezpieczeństwa, **zalecamy zmianę hasła po pierwszym logowaniu**.

Pozdrawiamy,
Administracja
""" 
        email_from = settings.DEFAULT_FROM_EMAIL 
        recipient_list = [user_email]

        try:
            send_mail(subject, message, email_from, recipient_list)
        except Exception:
            pass

    @transaction.atomic
    def create_single_user(self, coordinator: User, validated_data: dict) -> User:
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        provided_role = validated_data.get('role') 
        academic_title = validated_data.get('academic_title') 
        index_number = validated_data.get('index_number') 
        username_suggestion = validated_data.get('username', '') 

        if provided_role == Role.STUDENT:
            if academic_title is not None and academic_title != AcademicTitle.NONE:
                raise ValueError("Dane niespójne: Nie można utworzyć Studenta z tytułem naukowym.")
            if not index_number or not index_number.strip():
                raise ValueError("Dane niespójne: Dla roli Student wymagany jest numer indeksu.")

        elif provided_role == Role.SUPERVISOR:
            if academic_title is None or academic_title == AcademicTitle.NONE:
                raise ValueError("Dane niespójne: Dla roli Promotor wymagany jest tytuł naukowy.")
            if index_number and index_number.strip():
                raise ValueError("Dane niespójne: Promotor nie może mieć numeru indeksu.")

        username_to_use = username_suggestion.strip()

        if not username_to_use: 
            base_username = self.generate_username_from_names(first_name, last_name)
            username_to_use = base_username
            counter = 1
            while User.objects.filter(username=username_to_use).exists():
                username_to_use = f"{base_username}{counter}"
                counter += 1

        temporary_password = self.generate_temporary_password()

        try:
            new_user = User.objects.create_user(
                username=username_to_use,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=temporary_password, 
                role=provided_role, 
                academic_title=academic_title, 
                department=coordinator.department, 
            )

            if new_user.role == Role.STUDENT:
                StudentProfile.objects.create(
                    user=new_user,
                    index_number=index_number 
                )

            elif new_user.role == Role.SUPERVISOR:
                default_limits = getattr(settings, 'DEFAULT_SUPERVISOR_LIMITS', {})
                SupervisorProfile.objects.create(
                    user=new_user,
                    bacherol_limit=default_limits.get('bacherol_limit', 0),
                    engineering_limit=default_limits.get('engineering_limit', 0),
                    master_limit=default_limits.get('master_limit', 0),
                    phd_limit=default_limits.get('phd_limit', 0),
                )

            changed_fields_str = f'Koordynator o ID {coordinator.id} utworzył konto użytkownika {new_user.first_name} {new_user.last_name} (ID: {new_user.id}) z rolą {new_user.role.label} w dziale {new_user.department.name}.'

            Logs.objects.create(
                user_id=coordinator, 
                description=changed_fields_str,
                timestamp=timezone.now(),
            )

            self.send_welcome_email(
                user_email=new_user.email,
                username=new_user.username,
                temporary_password=temporary_password 
            )

            return new_user

        except IntegrityError as e:
            if 'username' in str(e).lower():
                raise ValueError(f"Użytkownik o nazwie użytkownika '{username_to_use}' już istnieje.")
            elif 'email' in str(e).lower():
                raise ValueError(f"Użytkownik o adresie email '{email}' już istnieje.")
            else:
                raise ValueError(f"Błąd unikalności podczas tworzenia użytkownika: {e}")

        except Exception as e:
            raise Exception("Wystąpił błąd podczas tworzenia konta użytkownika:.")

account_service = AccountCreationService()