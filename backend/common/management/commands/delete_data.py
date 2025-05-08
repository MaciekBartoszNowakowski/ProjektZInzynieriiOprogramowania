from django.core.management.base import BaseCommand
from users.models import User, StudentProfile, SupervisorProfile, Logs
from common.models import Department, Tag
from django.db import transaction

class Command(BaseCommand):
    help = 'Usuwa wszystkie dane testowe: użytkowników (oprócz superuserów), profile, wydziały, tagi, logi.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Usuwanie danych testowych...')

        with transaction.atomic():
            log_count, _ = Logs.objects.all().delete()
            self.stdout.write(f'Usunięto {log_count} obiektów Logs.')

            dept_count, _ = Department.objects.all().delete()
            self.stdout.write(f'Usunięto {dept_count} obiektów Department.')

            tag_count, _ = Tag.objects.all().delete()
            self.stdout.write(f'Usunięto {tag_count} obiektów Tag.')

            users_to_delete = User.objects.filter(is_superuser=False)
            user_count = users_to_delete.count()

            if user_count == 0:
                self.stdout.write('Nie znaleziono użytkowników (nie-superuserów) do usunięcia.')
            else:
                deleted_user_count, _ = users_to_delete.delete()
                self.stdout.write(f'Usunięto {deleted_user_count} użytkowników (nie-superuserów) wraz z powiązanymi profilami.')

        self.stdout.write(self.style.SUCCESS('Usuwanie danych testowych zakończone pomyślnie.'))