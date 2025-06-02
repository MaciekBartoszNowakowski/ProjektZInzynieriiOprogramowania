import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from users.models import User, Role, AcademicTitle, StudentProfile, SupervisorProfile
from common.models import Department, Tag
from thesis.models import Thesis, ThesisType, ThesisStatus
from applications.models import Submission

class Command(BaseCommand):
    help = 'Generuje dane testowe: użytkowników (Student, Supervisor, Koordynator), wydziały, tagi, prace dyplomowe i aplikacje.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generowanie danych...')

        with transaction.atomic():
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
            'Mikrokontrolery', 'Robotyka', 'Blockchain', 'IoT', 'Big Data', 'UI/UX',
            'Mobile Development', 'Game Development', 'Computer Vision', 'NLP'
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
        created_students = []
        
        existing_index_numbers = set(
            StudentProfile.objects.values_list('index_number', flat=True)
        )
        
        start_index = 100000
        while str(start_index) in existing_index_numbers:
            start_index += 1
            
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
            
            index_number = str(start_index + i)
            student_profile = StudentProfile.objects.create(user=user, index_number=index_number)
            created_students.append(student_profile)

            user.tags.set(random.sample(created_tags, random.randint(3, 8)))
            
            self.stdout.write(f'Utworzono studenta: {username}')

        self.stdout.write('Generowanie promotorów...')
        created_supervisors = []
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

            supervisor_profile = SupervisorProfile.objects.create(
                user=user,
                bacherol_limit=random.randint(1, 5),
                engineering_limit=random.randint(1, 5),
                master_limit=random.randint(1, 5),
                phd_limit=random.randint(0, 3),
            )
            created_supervisors.append(supervisor_profile)
            
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

        self.stdout.write('Tworzenie superużytkownika...')
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@agh.edu.pl',
                password='użytkownik',
                first_name='Admin',
                last_name='Systemowy',
                role=Role.ADMIN,
                academic_title=AcademicTitle.NONE,
                department=random.choice(created_departments)
            )
            self.stdout.write(self.style.SUCCESS('Superuser "admin" został utworzony.'))
        else:
            self.stdout.write('Superuser "admin" już istnieje.')

        thesis_topics = [
            "Zastosowanie sztucznej inteligencji w optymalizacji procesów biznesowych",
            "Analiza wydajności mikrousług w architekturze chmurowej",
            "Implementacja systemu IoT do monitorowania środowiska",
            "Bezpieczeństwo aplikacji webowych - analiza i przeciwdziałanie zagrożeniom",
            "Analiza danych w czasie rzeczywistym z wykorzystaniem Apache Kafka",
            "Rozwój aplikacji mobilnej z wykorzystaniem React Native",
            "System rekomendacji oparty na uczeniu maszynowym",
            "Blockchain w systemach zarządzania łańcuchem dostaw",
            "Analiza wydajności baz danych NoSQL",
            "Implementacja chatbota z wykorzystaniem NLP",
            "Automatyzacja testów w środowisku CI/CD",
            "Analiza obrazów medycznych z wykorzystaniem deep learning",
            "System zarządzania projektami z wykorzystaniem metodologii Agile",
            "Optymalizacja algorytmów sortowania dla dużych zbiorów danych",
            "Implementacja systemu płatności elektronicznych",
            "Analiza sentymentu w mediach społecznościowych",
            "System zarządzania treścią z wykorzystaniem headless CMS",
            "Aplikacja AR/VR do edukacji interaktywnej",
            "Monitoring i analiza wydajności aplikacji webowych",
            "System predykcji awarii w przemyśle 4.0"
        ]

        self.stdout.write('Generowanie prac dyplomowych...')
        created_theses = []
        
        for i in range(100):
            supervisor = random.choice(created_supervisors)
            thesis_type = random.choice(list(ThesisType))
            
            base_topic = random.choice(thesis_topics)
            if random.random() < 0.3:
                variations = [
                    f"{base_topic} - studium przypadku",
                    f"{base_topic} w środowisku przemysłowym",
                    f"{base_topic} - analiza porównawcza",
                    f"Innowacyjne podejście do {base_topic.lower()}",
                    f"{base_topic} - implementacja i ewaluacja"
                ]
                topic = random.choice(variations)
            else:
                topic = base_topic
            
            descriptions = [
                "Praca skupia się na teoretycznych podstawach oraz praktycznej implementacji rozwiązania.",
                "Celem pracy jest analiza, projektowanie i wdrożenie systemu spełniającego określone wymagania.",
                "Projekt obejmuje badanie istniejących rozwiązań oraz opracowanie nowego podejścia.",
                "Praca zawiera kompleksową analizę problemu i propozycję jego rozwiązania.",
                "Zadaniem jest zbadanie możliwości zastosowania nowoczesnych technologii w danej dziedzinie."
            ]
            
            status_weights = [0.6, 0.3, 0.1]
            status = random.choices(
                [ThesisStatus.APP_OPEN, ThesisStatus.APP_CLOSED, ThesisStatus.FINISHED],
                weights=status_weights
            )[0]
            
            thesis = Thesis.objects.create(
                supervisor_id=supervisor,
                thesis_type=thesis_type,
                name=topic,
                description=random.choice(descriptions),
                max_students=random.choices([1, 2], weights=[0.8, 0.2])[0],
                status=status,
                language=random.choices(
                    ["Polish", "English"], 
                    weights=[0.7, 0.3]
                )[0],
                updated_at=timezone.now()
            )
            
            thesis_tags = random.sample(created_tags, random.randint(2, 5))
            thesis.tags.set(thesis_tags)
            
            created_theses.append(thesis)
            self.stdout.write(f'Utworzono pracę: {topic[:50]}...')

        self.stdout.write('Generowanie aplikacji studentów...')
        
        students_with_applications = random.sample(created_students, min(50, len(created_students)))
        
        for student in students_with_applications:
            available_theses = [t for t in created_theses if t.status != ThesisStatus.FINISHED]
            
            if available_theses:
                if not Submission.objects.filter(student=student).exists():
                    thesis = random.choice(available_theses)
                    
                    current_submissions = Submission.objects.filter(thesis=thesis).count()
                    if current_submissions < thesis.max_students:
                        Submission.objects.create(
                            student=student,
                            thesis=thesis
                        )
                        self.stdout.write(f'Utworzono aplikację: {student.user.username} -> {thesis.name[:30]}...')
                        
                        if current_submissions + 1 >= thesis.max_students and thesis.status == ThesisStatus.APP_OPEN:
                            thesis.status = ThesisStatus.APP_CLOSED
                            thesis.save()

        self.stdout.write(self.style.SUCCESS('\nGenerowanie danych zakończone pomyślnie!'))
        self.stdout.write(self.style.SUCCESS('Domyślne hasło dla wszystkich wygenerowanych użytkowników: użytkownik'))
        
        # Podsumowanie utworzonych danych
        self.stdout.write(self.style.SUCCESS('\nPodsumowanie:'))
        self.stdout.write(f'- Użytkownicy: {User.objects.filter(is_superuser=False).count()} + 1 admin')
        self.stdout.write(f'- Studenci: {StudentProfile.objects.count()}')
        self.stdout.write(f'- Promotorzy: {SupervisorProfile.objects.count()}')
        self.stdout.write(f'- Wydziały: {len(created_departments)}')
        self.stdout.write(f'- Tagi: {len(created_tags)}')
        self.stdout.write(f'- Prace dyplomowe: {Thesis.objects.count()}')
        self.stdout.write(f'- Aplikacje studentów: {Submission.objects.count()}')
