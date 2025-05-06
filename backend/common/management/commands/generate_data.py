import random
import string
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from users.models import User, Role, AcademicTitle, StudentProfile, SupervisorProfile
from common.models import Department, Tag

class Command(BaseCommand):
    help = 'Generuje dane testowe: użytkowników (Student, Supervisor, Koordynator), wydziały i tagi.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generowanie danych...')

        departments = [
            'Wydział Informatyki',
            'Wydział Elektrotechniki, Automatyki, Informatyki i Inżynierii Biomedycznej',
            'Wydział Inżynierii Mechanicznej i Robotyki',
        ]
        created_departments = []
        for name in departments:
            department, created = Department.objects.get_or_create(name=name, defaults={'description': f'Opis wydziału {name}'})
            created_departments.append(department)
            if created:
                self.stdout.write(f'Utworzono wydział: {name}')
            else:
                self.stdout.write(f'Wydział już istnieje: {name}')

        tags = [
            'Python', 'Django', 'REST API', 'Bazy Danych', 'JavaScript', 'React', 'Angular', 'Vue.js',
            'Docker', 'Kubernetes', 'Chmura', 'AI', 'Machine Learning', 'Sieci Neuronowe',
            'Cyberbezpieczeństwo', 'Analiza Danych', 'Testowanie Oprogramowania', 'DevOps',
            'Mikrokontrolery', 'Robotyka'
        ]
        created_tags = []
        for name in tags:
            tag, created = Tag.objects.get_or_create(name=name)
            created_tags.append(tag)
            if created:
                self.stdout.write(f'Utworzono tag: {name}')
            else:
                self.stdout.write(f'Tag już istnieje: {name}')

        polish_first_names = ['Jan', 'Anna', 'Piotr', 'Maria', 'Krzysztof', 'Katarzyna', 'Andrzej', 'Małgorzata', 'Michał', 'Agnieszka', 'Tomasz', 'Barbara']
        polish_last_names = ['Kowalski', 'Nowak', 'Wiśniewski', 'Wójcik', 'Kowalczyk', 'Kamiński', 'Zieliński', 'Szymański', 'Woźniak', 'Dąbrowski', 'Kozłowski', 'Jankowski']

        def clean_polish_chars(text):
            replacements = {
                'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
                'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
                'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
                'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z',
            }
            for old, new in replacements.items():
                text = text.replace(old, new)
            return text

        def generate_username(first, last, counter=0):
            base = f"{clean_polish_chars(first).lower()[0]}{clean_polish_chars(last).lower()}"
            base = base.replace('-', '')
            if counter > 0:
                base = f"{base[:15]}{counter}"
            return base[:150]

        def get_unique_username(first, last):
            counter = 0
            while True:
                username = generate_username(first, last, counter)
                if not User.objects.filter(username=username).exists():
                    return username
                counter += 1

        def get_random_name():
            first = random.choice(polish_first_names)
            last = random.choice(polish_last_names)
            return first, last

        self.stdout.write('Generowanie studentów...')
        for i in range(100):
            first_name, last_name = get_random_name()
            username = get_unique_username(first_name, last_name)
            email = f"{username}@student.agh.edu.pl"
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=Role.STUDENT,
                academic_title=random.choice([AcademicTitle.ENGINEER, AcademicTitle.BACHELOR, AcademicTitle.NONE]),
                department=random.choice(created_departments),
                password='użytkownik',
                updated_at=timezone.now()
            )
            
            index_number = str(100000 + i)
            StudentProfile.objects.create(user=user, index_number=index_number)

            user.tags.set(random.sample(created_tags, random.randint(3, 8)))
            
            self.stdout.write(f'Utworzono studenta: {username}')

        self.stdout.write('Generowanie promotorów...')
        for i in range(20):
            first_name, last_name = get_random_name()
            username = get_unique_username(first_name, last_name)
            email = f"{username}@agh.edu.pl"

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=Role.SUPERVISOR,
                academic_title=random.choice([AcademicTitle.DOCTOR, AcademicTitle.HABILITATED_DOCTOR, AcademicTitle.PROFESSOR]),
                department=random.choice(created_departments),
                password='użytkownik',
                updated_at=timezone.now()
            )

            SupervisorProfile.objects.create(
                user=user,
                bacherol_limit=random.randint(1, 5),
                engineering_limit=random.randint(1, 5),
                master_limit=random.randint(1, 5),
                phd_limit=random.randint(0, 3),
            )
            
            user.tags.set(random.sample(created_tags, random.randint(5, 12)))
            
            self.stdout.write(f'Utworzono promotora: {username}')

        self.stdout.write('Generowanie koordynatorów...')
        for i in range(3):
            first_name, last_name = get_random_name()
            username = get_unique_username(first_name, last_name)
            email = f"{username}@agh.edu.pl"

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=Role.COORDINATOR,
                academic_title=random.choice([AcademicTitle.NONE, AcademicTitle.MASTER, AcademicTitle.DOCTOR]),
                 department=random.choice(created_departments),
                password='użytkownik',
                updated_at=timezone.now()
            )

            user.tags.set(random.sample(created_tags, random.randint(2, 6)))

            self.stdout.write(f'Utworzono koordynatora: {username}')

        self.stdout.write(self.style.SUCCESS('\nGenerowanie danych zakończone pomyślnie!'))
        self.stdout.write(self.style.SUCCESS('Domyślne hasło dla wszystkich wygenerowanych użytkowników: użytkownik'))