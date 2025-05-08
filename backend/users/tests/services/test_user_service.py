from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from users.models import Role, AcademicTitle, StudentProfile, SupervisorProfile, Logs
from common.models import Department, Tag
from users.services.user_service import user_service

User = get_user_model()

class UserServiceTests(TestCase):

    def setUp(self):
        self.department_it = Department.objects.create(name="Wydział IT")
        self.tag_python = Tag.objects.create(name="Python")
        self.tag_django = Tag.objects.create(name="Django")
        self.tag_rest = Tag.objects.create(name="REST API") 
        self.tag_db = Tag.objects.create(name="Bazy Danych")

        self.student_password = 'student_password'
        self.user_student = User.objects.create_user(
            username='student_test', password=self.student_password, email='s.test@example.com',
            first_name='Student', last_name='Testowy', role=Role.STUDENT,
            description='Initial student description', department=self.department_it
        )
        self.student_profile = StudentProfile.objects.create(
            user=self.user_student, index_number='S12345'
        )
        self.user_student.tags.add(self.tag_python)

        self.supervisor_password = 'supervisor_password'
        self.user_supervisor = User.objects.create_user(
            username='supervisor_test', password=self.supervisor_password, email='p.test@example.com',
            first_name='Promotor', last_name='Testowy', role=Role.SUPERVISOR,
            academic_title=AcademicTitle.DOCTOR, description='Initial supervisor description',
            department=self.department_it
        )
        self.supervisor_profile = SupervisorProfile.objects.create(
            user=self.user_supervisor, bacherol_limit=2, engineering_limit=3, master_limit=4, phd_limit=1
        )
        self.user_supervisor.tags.add(self.tag_python, self.tag_django)

        self.coordinator_password = 'coordinator_password'
        self.user_coordinator = User.objects.create_user(
            username='coordinator_test', password=self.coordinator_password, email='k.test@example.com',
            first_name='Koordynator', last_name='Testowy', role=Role.COORDINATOR,
            description='Initial coordinator description', department=self.department_it
        )

        self.admin_password = 'admin_password'
        self.user_admin = User.objects.create_user(
            username='admin_test', password=self.admin_password, email='a.test@example.com',
            first_name='Admin', last_name='Testowy', role=Role.ADMIN,
            description='Initial admin description', department=self.department_it
        )

    def test_update_student_description(self):
        initial_description = self.user_student.description
        new_description = "Updated student description via service"
        validated_data = {
            'user': {'description': new_description}
        }

        self.assertEqual(Logs.objects.count(), 0)

        updated_user = user_service.update_user_data(self.user_student, validated_data)

        self.user_student.refresh_from_db()

        self.assertEqual(self.user_student.description, new_description)
        self.assertEqual(updated_user.description, new_description)

        self.student_profile.refresh_from_db()
        self.assertEqual(self.student_profile.index_number, 'S12345')

        self.assertEqual(Logs.objects.count(), 1)
        log_entry = Logs.objects.first()
        self.assertEqual(log_entry.user_id, self.user_student)

        expected_log_part = f'User.description: z "{initial_description}" na "{new_description}"'
        self.assertIn(expected_log_part, log_entry.description)
        self.assertNotIn('StudentProfile.', log_entry.description)

    def test_update_student_ignores_other_user_fields(self):
        initial_username = self.user_student.username
        initial_role = self.user_student.role
        initial_description = self.user_student.description 
        validated_data = {
            'user': {
                'username': 'new_student_username',
                'role': Role.SUPERVISOR,
            }
        }

        self.assertEqual(Logs.objects.count(), 0)

        user_service.update_user_data(self.user_student, validated_data)

        self.user_student.refresh_from_db()

        self.assertEqual(self.user_student.description, initial_description)
        self.assertEqual(self.user_student.username, initial_username) 
        self.assertEqual(self.user_student.role, initial_role) 

        self.assertEqual(Logs.objects.count(), 0) 

    def test_update_student_ignores_profile_fields(self):
        initial_description = self.user_student.description
        initial_index_number = self.student_profile.index_number
        validated_data = {
            'index_number': 'S99999',
        }

        self.assertEqual(Logs.objects.count(), 0)

        user_service.update_user_data(self.user_student, validated_data)

        self.user_student.refresh_from_db()
        self.student_profile.refresh_from_db()

        self.assertEqual(self.user_student.description, initial_description)
        self.assertEqual(self.student_profile.index_number, initial_index_number)

        self.assertEqual(Logs.objects.count(), 0)


    def test_update_student_with_empty_data(self):
        initial_description = self.user_student.description
        initial_index_number = self.student_profile.index_number
        validated_data = {}

        self.assertEqual(Logs.objects.count(), 0)

        user_service.update_user_data(self.user_student, validated_data)

        self.user_student.refresh_from_db()
        self.student_profile.refresh_from_db()

        self.assertEqual(self.user_student.description, initial_description)
        self.assertEqual(self.student_profile.index_number, initial_index_number)

        self.assertEqual(Logs.objects.count(), 0)


    def test_update_supervisor_description(self):
        initial_description = self.user_supervisor.description
        new_description = "Updated supervisor description via service"
        validated_data = {
            'user': {'description': new_description}
        }

        self.assertEqual(Logs.objects.count(), 0)

        user_service.update_user_data(self.user_supervisor, validated_data)

        self.user_supervisor.refresh_from_db()
        self.supervisor_profile.refresh_from_db()

        self.assertEqual(self.user_supervisor.description, new_description)
        self.assertEqual(self.supervisor_profile.bacherol_limit, 2)

        self.assertEqual(Logs.objects.count(), 1)
        log_entry = Logs.objects.first()
        self.assertIn('User.description', log_entry.description)
        self.assertNotIn('SupervisorProfile.', log_entry.description)

    def test_update_supervisor_limits(self):
        initial_description = self.user_supervisor.description
        new_bacherol_limit = 100
        new_master_limit = 150
        validated_data = {
            'bacherol_limit': new_bacherol_limit,
            'master_limit': new_master_limit,
        }

        self.assertEqual(Logs.objects.count(), 0)

        user_service.update_user_data(self.user_supervisor, validated_data)

        self.user_supervisor.refresh_from_db()
        self.supervisor_profile.refresh_from_db()

        self.assertEqual(self.supervisor_profile.bacherol_limit, new_bacherol_limit)
        self.assertEqual(self.supervisor_profile.master_limit, new_master_limit)
        self.assertEqual(self.supervisor_profile.engineering_limit, 3)
        self.assertEqual(self.user_supervisor.description, initial_description)

        self.assertEqual(Logs.objects.count(), 1)
        log_entry = Logs.objects.first()
        self.assertNotIn('User.description', log_entry.description)
        self.assertIn('SupervisorProfile.bacherol_limit', log_entry.description)
        self.assertIn('SupervisorProfile.master_limit', log_entry.description)
        self.assertNotIn('SupervisorProfile.engineering_limit', log_entry.description)

    def test_update_supervisor_description_and_limits_together(self):
        initial_bacherol_limit = self.supervisor_profile.bacherol_limit
        new_description = "Combined update test"
        new_engineering_limit = 777
        validated_data = {
            'user': {'description': new_description},
            'engineering_limit': new_engineering_limit,
        }

        self.assertEqual(Logs.objects.count(), 0)

        user_service.update_user_data(self.user_supervisor, validated_data)

        self.user_supervisor.refresh_from_db()
        self.supervisor_profile.refresh_from_db()

        self.assertEqual(self.user_supervisor.description, new_description)
        self.assertEqual(self.supervisor_profile.engineering_limit, new_engineering_limit)
        self.assertEqual(self.supervisor_profile.bacherol_limit, initial_bacherol_limit)

        self.assertEqual(Logs.objects.count(), 1)
        log_entry = Logs.objects.first()
        self.assertIn('User.description', log_entry.description)
        self.assertIn('SupervisorProfile.engineering_limit', log_entry.description)
        self.assertNotIn('SupervisorProfile.bacherol_limit', log_entry.description)

    def test_update_supervisor_ignores_other_user_fields(self):
        initial_username = self.user_supervisor.username
        initial_academic_title = self.user_supervisor.academic_title
        initial_bacherol_limit = self.supervisor_profile.bacherol_limit
        validated_data = {
            'user': {
                'description': 'Supervisor description update attempt',
                'username': 'new_supervisor_username',
                'academic_title': AcademicTitle.PROFESSOR,
            },
        }

        self.assertEqual(Logs.objects.count(), 0)

        user_service.update_user_data(self.user_supervisor, validated_data)

        self.user_supervisor.refresh_from_db()
        self.supervisor_profile.refresh_from_db()

        self.assertEqual(self.user_supervisor.description, 'Supervisor description update attempt')
        self.assertEqual(self.user_supervisor.username, initial_username) 
        self.assertEqual(self.user_supervisor.academic_title, initial_academic_title) 
        self.assertEqual(self.supervisor_profile.bacherol_limit, initial_bacherol_limit)

        self.assertEqual(Logs.objects.count(), 1)
        log_entry = Logs.objects.first()
        self.assertIn('User.description', log_entry.description)
        self.assertNotIn('User.username', log_entry.description)
        self.assertNotIn('SupervisorProfile.', log_entry.description)

    def test_update_supervisor_ignores_profile_fields_if_not_in_validated_data(self):
        initial_description = self.user_supervisor.description
        initial_bacherol_limit = self.supervisor_profile.bacherol_limit
        validated_data = {
             'user': {'description': 'Only description'}
        }

        self.assertEqual(Logs.objects.count(), 0)
        user_service.update_user_data(self.user_supervisor, validated_data)
        self.user_supervisor.refresh_from_db()
        self.supervisor_profile.refresh_from_db()

        self.assertEqual(self.user_supervisor.description, 'Only description')
        self.assertEqual(self.supervisor_profile.bacherol_limit, initial_bacherol_limit) 

        self.assertEqual(Logs.objects.count(), 1) 

    def test_update_supervisor_with_empty_data(self):
        initial_description = self.user_supervisor.description
        initial_bacherol_limit = self.supervisor_profile.bacherol_limit
        validated_data = {}

        self.assertEqual(Logs.objects.count(), 0)

        user_service.update_user_data(self.user_supervisor, validated_data)

        self.user_supervisor.refresh_from_db()
        self.supervisor_profile.refresh_from_db()

        self.assertEqual(self.user_supervisor.description, initial_description)
        self.assertEqual(self.supervisor_profile.bacherol_limit, initial_bacherol_limit)

        self.assertEqual(Logs.objects.count(), 0) 

    def test_update_coordinator_description(self):
        initial_description = self.user_coordinator.description
        new_description = "Updated coordinator description via service"
        validated_data = {
            'description': new_description
        }

        self.assertEqual(Logs.objects.count(), 0)

        user_service.update_user_data(self.user_coordinator, validated_data)

        self.user_coordinator.refresh_from_db()

        self.assertEqual(self.user_coordinator.description, new_description)

        self.assertEqual(Logs.objects.count(), 1)
        log_entry = Logs.objects.first()
        self.assertIn('User.description', log_entry.description)
        self.assertNotIn('SupervisorProfile.', log_entry.description)

    def test_update_admin_ignores_other_user_fields(self):
        initial_email = self.user_admin.email
        initial_first_name = self.user_admin.first_name
        initial_description = self.user_admin.description
        validated_data = {
            'email': 'new_admin_email@example.com',
            'first_name': 'Nowe Imie Admina',
        }

        self.assertEqual(Logs.objects.count(), 0)

        user_service.update_user_data(self.user_admin, validated_data)

        self.user_admin.refresh_from_db()

        self.assertEqual(self.user_admin.description, initial_description)
        self.assertEqual(self.user_admin.email, initial_email) 
        self.assertEqual(self.user_admin.first_name, initial_first_name)

        self.assertEqual(Logs.objects.count(), 0) 


    def test_update_coordinator_with_empty_data(self):
        initial_description = self.user_coordinator.description
        validated_data = {}

        self.assertEqual(Logs.objects.count(), 0)

        user_service.update_user_data(self.user_coordinator, validated_data)

        self.user_coordinator.refresh_from_db()

        self.assertEqual(self.user_coordinator.description, initial_description)

        self.assertEqual(Logs.objects.count(), 0) 

    def test_update_supervisor_without_profile_handles_gracefully(self):
        user_sup_no_profile = User.objects.create_user(
            username='sup_no_profile', password='password', email='snp@example.com',
            first_name='No', last_name='Profile', role=Role.SUPERVISOR,
            description='Initial desc', department=self.department_it
        )

        initial_description = user_sup_no_profile.description
        new_description = "Updated desc for sup without profile"
        validated_data = {'user': {'description': new_description}}

        self.assertEqual(Logs.objects.count(), 0)

        user_service.update_user_data(user_sup_no_profile, validated_data)

        user_sup_no_profile.refresh_from_db()

        self.assertEqual(user_sup_no_profile.description, new_description)
        self.assertFalse(hasattr(user_sup_no_profile, 'supervisorprofile'))

        self.assertEqual(Logs.objects.count(), 1)
        log_entry = Logs.objects.first()
        self.assertIn('User.description', log_entry.description)
        self.assertNotIn('SupervisorProfile.', log_entry.description)

    def test_update_user_tags_adds_tags(self):
        user = self.user_student
        initial_tag_names = sorted([tag.name for tag in user.tags.all()])
        self.assertListEqual(initial_tag_names, sorted([self.tag_python.name]))

        tags_to_add = [self.tag_django, self.tag_rest]
        validated_data = {'to_add': tags_to_add}

        self.assertEqual(Logs.objects.count(), 0)

        updated_tags = user_service.update_user_tags(user, validated_data)

        user.refresh_from_db()
        updated_tag_names = sorted([tag.name for tag in user.tags.all()])

        self.assertListEqual(updated_tag_names, sorted([self.tag_python.name, self.tag_django.name, self.tag_rest.name]))
        self.assertListEqual(sorted([tag.name for tag in updated_tags]), updated_tag_names) 

        self.assertEqual(Logs.objects.count(), 1)
        log_entry = Logs.objects.first()
        self.assertEqual(log_entry.user_id, user)
        self.assertIn('Użytkownik o ID:', log_entry.description)
        self.assertIn(f'({user.username}) zmienił tagi.', log_entry.description)
        self.assertIn('Dodano tagi: Django, REST API', log_entry.description)
        self.assertNotIn('Usunięto tagi:', log_entry.description)

    def test_update_user_tags_removes_tags(self):
        user = self.user_supervisor
        initial_tag_names = sorted([tag.name for tag in user.tags.all()])
        self.assertListEqual(initial_tag_names, sorted([self.tag_python.name, self.tag_django.name]))

        tags_to_remove = [self.tag_python]
        validated_data = {'to_remove': tags_to_remove}

        self.assertEqual(Logs.objects.count(), 0)

        updated_tags = user_service.update_user_tags(user, validated_data)

        user.refresh_from_db()
        updated_tag_names = sorted([tag.name for tag in user.tags.all()])

        self.assertListEqual(updated_tag_names, sorted([self.tag_django.name]))
        self.assertListEqual(sorted([tag.name for tag in updated_tags]), updated_tag_names)

        self.assertEqual(Logs.objects.count(), 1)
        log_entry = Logs.objects.first()
        self.assertEqual(log_entry.user_id, user)
        self.assertIn('Użytkownik o ID:', log_entry.description)
        self.assertIn(f'({user.username}) zmienił tagi.', log_entry.description)
        self.assertIn('Usunięto tagi: Python', log_entry.description)
        self.assertNotIn('Dodano tagi:', log_entry.description)


    def test_update_user_tags_adds_and_removes(self):
        user = self.user_supervisor 
        initial_tag_names = sorted([tag.name for tag in user.tags.all()])
        self.assertListEqual(initial_tag_names, sorted([self.tag_python.name, self.tag_django.name]))

        tags_to_add = [self.tag_rest]
        tags_to_remove = [self.tag_python]
        validated_data = {'to_add': tags_to_add, 'to_remove': tags_to_remove}

        self.assertEqual(Logs.objects.count(), 0)

        updated_tags = user_service.update_user_tags(user, validated_data)

        user.refresh_from_db()
        updated_tag_names = sorted([tag.name for tag in user.tags.all()])

        self.assertListEqual(updated_tag_names, sorted([self.tag_django.name, self.tag_rest.name]))
        self.assertListEqual(sorted([tag.name for tag in updated_tags]), updated_tag_names)

        self.assertEqual(Logs.objects.count(), 1)
        log_entry = Logs.objects.first()
        self.assertEqual(log_entry.user_id, user)
        self.assertIn('Dodano tagi: REST API', log_entry.description)
        self.assertIn('Usunięto tagi: Python', log_entry.description)
        self.assertIn(' | ', log_entry.description)


    def test_update_user_tags_with_empty_lists(self):
        user = self.user_student
        initial_tag_names = sorted([tag.name for tag in user.tags.all()])
        self.assertListEqual(initial_tag_names, sorted([self.tag_python.name]))

        validated_data = {'to_add': [], 'to_remove': []}

        self.assertEqual(Logs.objects.count(), 0)

        updated_tags = user_service.update_user_tags(user, validated_data)

        user.refresh_from_db()
        updated_tag_names = sorted([tag.name for tag in user.tags.all()])

        self.assertListEqual(updated_tag_names, initial_tag_names)
        self.assertListEqual(sorted([tag.name for tag in updated_tags]), initial_tag_names)

        self.assertEqual(Logs.objects.count(), 0)


    def test_update_user_tags_with_missing_keys(self):
        user = self.user_student
        initial_tag_names = sorted([tag.name for tag in user.tags.all()])

        validated_data1 = {'to_add': [self.tag_django, self.tag_rest]}
        self.assertEqual(Logs.objects.count(), 0)
        user_service.update_user_tags(user, validated_data1)
        user.refresh_from_db()
        self.assertListEqual(sorted([tag.name for tag in user.tags.all()]), sorted([self.tag_python.name, self.tag_django.name, self.tag_rest.name]))
        self.assertEqual(Logs.objects.count(), 1)
        Logs.objects.all().delete()

        user_sup = self.user_supervisor
        initial_sup_tag_names = sorted([tag.name for tag in user_sup.tags.all()])
        self.assertListEqual(initial_sup_tag_names, sorted([self.tag_python.name, self.tag_django.name]))

        validated_data2 = {'to_remove': [self.tag_python]}
        self.assertEqual(Logs.objects.count(), 0)
        user_service.update_user_tags(user_sup, validated_data2)
        user_sup.refresh_from_db()
        self.assertListEqual(sorted([tag.name for tag in user_sup.tags.all()]), sorted([self.tag_django.name]))
        self.assertEqual(Logs.objects.count(), 1)
        Logs.objects.all().delete()

        user_student_copy = User.objects.get(pk=self.user_student.pk)
        initial_student_tag_names = sorted([tag.name for tag in user_student_copy.tags.all()])
        validated_data3 = {}
        self.assertEqual(Logs.objects.count(), 0)
        user_service.update_user_tags(user_student_copy, validated_data3)
        user_student_copy.refresh_from_db()
        self.assertListEqual(sorted([tag.name for tag in user_student_copy.tags.all()]), initial_student_tag_names)
        self.assertEqual(Logs.objects.count(), 0)


    def test_update_user_tags_no_change_logging(self):
        user = self.user_student

        tags_to_add_existing = [self.tag_python]
        validated_data1 = {'to_add': tags_to_add_existing}
        self.assertEqual(Logs.objects.count(), 0)
        user_service.update_user_tags(user, validated_data1)
        self.assertEqual(Logs.objects.count(), 0)

        tags_to_remove_non_existing = [self.tag_rest]
        validated_data2 = {'to_remove': tags_to_remove_non_existing}
        self.assertEqual(Logs.objects.count(), 0)
        user_service.update_user_tags(user, validated_data2)
        self.assertEqual(Logs.objects.count(), 0)

        validated_data3 = {'to_add': [self.tag_python], 'to_remove': [self.tag_rest]}
        self.assertEqual(Logs.objects.count(), 0)
        user_service.update_user_tags(user, validated_data3)
        self.assertEqual(Logs.objects.count(), 0)


    def test_update_user_tags_logging_format(self):
        user = self.user_student
        
        tags_to_add = [self.tag_django]
        tags_to_remove = [self.tag_python]

        validated_data = {'to_add': tags_to_add, 'to_remove': tags_to_remove}

        user_service.update_user_tags(user, validated_data)
        
        self.assertEqual(Logs.objects.count(), 1)
        log_entry = Logs.objects.first()
        
        self.assertIn(f'Użytkownik o ID: {user.id} ({user.username}) zmienił tagi.', log_entry.description)
        self.assertIn('Dodano tagi: Django', log_entry.description)
        self.assertIn('Usunięto tagi: Python', log_entry.description)
        self.assertIn(' | ', log_entry.description)

        Logs.objects.all().delete()
        user.tags.remove(self.tag_django)
        user.tags.add(self.tag_python)

        validated_data_add_only = {'to_add': [self.tag_django, self.tag_rest], 'to_remove': []}
        user_service.update_user_tags(user, validated_data_add_only)
        self.assertEqual(Logs.objects.count(), 1)
        log_entry_add = Logs.objects.first()
        self.assertIn('Dodano tagi: Django, REST API', log_entry_add.description)
        self.assertNotIn('Usunięto tagi:', log_entry_add.description)

        Logs.objects.all().delete()
        user.tags.add(self.tag_django, self.tag_rest)
        
        validated_data_remove_only = {'to_add': [], 'to_remove': [self.tag_django, self.tag_rest]}
        user_service.update_user_tags(user, validated_data_remove_only)
        self.assertEqual(Logs.objects.count(), 1)
        log_entry_remove = Logs.objects.first()
        self.assertNotIn('Dodano tagi:', log_entry_remove.description)
        self.assertIn('Usunięto tagi: Django, REST API', log_entry_remove.description)