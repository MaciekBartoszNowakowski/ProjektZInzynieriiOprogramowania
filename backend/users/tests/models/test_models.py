from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError, DataError
from django.utils import timezone
from users.models import StudentProfile, SupervisorProfile, Role, AcademicTitle, Logs
from common.models import Department, Tag
from django.db import transaction

User = get_user_model()

class BaseModelTests(TestCase):
    def setUp(self):
        self.department_it = Department.objects.create(name="Wydział IT", description="Wydział Informatyki")
        self.department_el = Department.objects.create(name="Wydział EL", description="Wydział Elektryczny")

        self.tag_python = Tag.objects.create(name="Python")
        self.tag_django = Tag.objects.create(name="Django")
        self.tag_ai = Tag.objects.create(name="AI")


        self.student_user = User.objects.create_user(username='student_user', password='password123', role=Role.STUDENT, department=self.department_it, first_name="Jan", last_name="Student")
        self.supervisor_user = User.objects.create_user(username='supervisor_user', password='password123', role=Role.SUPERVISOR, department=self.department_el, academic_title=AcademicTitle.DOCTOR, first_name="Anna", last_name="Promotor")
        self.coordinator_user = User.objects.create_user(username='coordinator_user', password='password123', role=Role.COORDINATOR, first_name="Piotr", last_name="Koordynator")
        self.admin_user = User.objects.create_superuser(username='admin_user', password='password123', first_name="Adam", last_name="Admin")
        self.basic_user = User.objects.create_user(username='basic_user', password='password123')

        self.supervisor_user.tags.add(self.tag_python, self.tag_django)
        self.basic_user.tags.add(self.tag_ai)

        self.student_profile = StudentProfile.objects.create(user=self.student_user, index_number='S12345')
        self.supervisor_profile = SupervisorProfile.objects.create(user=self.supervisor_user)

class DepartmentModelTests(BaseModelTests):
    def test_department_creation(self):
        self.assertEqual(Department.objects.count(), 2)
        self.assertEqual(self.department_it.name, "Wydział IT")
        self.assertEqual(self.department_el.description, "Wydział Elektryczny")

    def test_department_str_representation(self):
        expected_str = f"Wydział: {self.department_it.name} \nOpis: {self.department_it.description}"
        self.assertEqual(str(self.department_it), expected_str)

class TagModelTests(BaseModelTests):
    def test_tag_creation(self):
        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(self.tag_python.name, "Python")
        self.assertEqual(self.tag_django.name, "Django")
        self.assertEqual(self.tag_ai.name, "AI")

    def test_tag_str_representation(self):
        self.assertEqual(str(self.tag_python), "Python")
        self.assertEqual(str(self.tag_django), "Django")
        self.assertEqual(str(self.tag_ai), "AI")


class UserModelTests(BaseModelTests):
    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 5)

        self.assertTrue(self.student_user.check_password('password123'))
        self.assertEqual(self.student_user.role, Role.STUDENT)
        self.assertEqual(self.student_user.department.name, "Wydział IT")
        self.assertEqual(self.student_user.first_name, "Jan")
        self.assertEqual(self.student_user.last_name, "Student")

        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)
        self.assertEqual(self.admin_user.role, Role.STUDENT)
        self.assertIsNone(self.admin_user.department)

    def test_user_defaults(self):
        user = User.objects.create_user(username='defaults_user', password='pwd')
        self.assertEqual(user.role, Role.STUDENT)
        self.assertEqual(user.academic_title, AcademicTitle.NONE)
        self.assertEqual(user.description, "")
        self.assertIsNotNone(user.updated_at)
        self.assertIsNone(user.department)
        self.assertEqual(user.tags.count(), 0)

    def test_user_nullable_fields(self):
        user = User.objects.create_user(
            username='nullable_user',
            password='pwd',
            role=None,
            academic_title=None,
            description=None,
            department=None
        )
        self.assertIsNone(user.role)
        self.assertIsNone(user.academic_title)
        self.assertIsNone(user.description)
        self.assertIsNone(user.department)
        self.assertEqual(user.tags.count(), 0)

        user_empty_desc = User.objects.create_user(
            username='empty_desc_user',
            password='pwd',
            description=""
        )
        self.assertEqual(user_empty_desc.description, "")
        self.assertIsNotNone(user_empty_desc.description)

    def test_user_department_relation(self):
        user = User.objects.get(username='student_user')
        self.assertEqual(user.department.name, "Wydział IT")

    def test_user_department_on_delete_set_null(self):
        user = User.objects.get(username='student_user')
        department_id = user.department.id

        self.assertIsNotNone(Department.objects.get(id=department_id))

        Department.objects.get(id=department_id).delete()

        user.refresh_from_db()

        self.assertIsNone(user.department)

        with self.assertRaises(Department.DoesNotExist):
             Department.objects.get(id=department_id)

    def test_user_str_representation(self):
        self.assertEqual(str(self.student_user), 'Profil użytkownika: Jan Student')
        self.assertEqual(str(self.supervisor_user), 'Profil użytkownika: doktor Anna Promotor')
        user_no_name = User.objects.create_user(username='no_name_user', password='pwd', academic_title=AcademicTitle.NONE, first_name='', last_name='')
        self.assertEqual(str(user_no_name), 'Profil użytkownika:  ')

    def test_user_tags_relation(self):
        supervisor = User.objects.get(username='supervisor_user')
        basic_user = User.objects.get(username='basic_user')
        student = User.objects.get(username='student_user')

        self.assertEqual(
            sorted(list(supervisor.tags.all()), key=lambda tag: tag.name),
            sorted([self.tag_django, self.tag_python], key=lambda tag: tag.name)
        )
        self.assertEqual(
            sorted(list(basic_user.tags.all()), key=lambda tag: tag.name),
            sorted([self.tag_ai], key=lambda tag: tag.name)
        )
        self.assertEqual(student.tags.count(), 0)

        student.tags.add(self.tag_python)
        self.assertIn(self.tag_python, student.tags.all())
        self.assertEqual(student.tags.count(), 1)

        student.tags.add(self.tag_django, self.tag_ai)
        self.assertEqual(student.tags.count(), 3)
        self.assertIn(self.tag_django, student.tags.all())
        self.assertIn(self.tag_ai, student.tags.all())

        student.tags.remove(self.tag_python)
        self.assertEqual(student.tags.count(), 2)
        self.assertNotIn(self.tag_python, student.tags.all())

        student.tags.clear()
        self.assertEqual(student.tags.count(), 0)

    def test_tag_users_related_name(self):
        python_tag = Tag.objects.get(name="Python")
        django_tag = Tag.objects.get(name="Django")
        ai_tag = Tag.objects.get(name="AI")

        self.assertIn(self.supervisor_user, python_tag.users.all())
        self.assertIn(self.supervisor_user, django_tag.users.all())
        self.assertNotIn(self.supervisor_user, ai_tag.users.all())

        self.assertNotIn(self.student_user, python_tag.users.all())
        self.assertNotIn(self.student_user, django_tag.users.all())
        self.assertNotIn(self.student_user, ai_tag.users.all())

        self.assertNotIn(self.basic_user, python_tag.users.all())
        self.assertNotIn(self.basic_user, django_tag.users.all())
        self.assertIn(self.basic_user, ai_tag.users.all())

        self.student_user.tags.add(self.tag_python)
        self.assertIn(self.student_user, python_tag.users.all())

        self.supervisor_user.tags.remove(self.tag_django)
        self.assertNotIn(self.supervisor_user, django_tag.users.all())

    def test_user_deletion_does_not_delete_tags(self):
        user_with_tags = User.objects.create_user(username='user_tags_del', password='pwd')
        user_with_tags.tags.add(self.tag_python, self.tag_ai)
        tag_count_before = Tag.objects.count()

        user_with_tags.delete()

        self.assertEqual(Tag.objects.count(), tag_count_before)
        python_tag = Tag.objects.get(name="Python")
        ai_tag = Tag.objects.get(name="AI")
        self.assertNotIn(user_with_tags, python_tag.users.all())
        self.assertNotIn(user_with_tags, ai_tag.users.all())


    def test_tag_deletion_does_not_delete_users(self):
        user_with_tags = User.objects.create_user(username='tag_del_user', password='pwd')
        tag_to_delete = Tag.objects.create(name="TemporaryTag")
        user_with_tags.tags.add(tag_to_delete)

        user_count_before = User.objects.count()

        tag_to_delete.delete()

        self.assertEqual(User.objects.count(), user_count_before)
        user_with_tags.refresh_from_db()
        self.assertNotIn(tag_to_delete, user_with_tags.tags.all())


class StudentProfileModelTests(BaseModelTests):
    def test_student_profile_creation(self):
        self.assertEqual(StudentProfile.objects.count(), 1)
        profile = StudentProfile.objects.get(user=self.student_user)
        self.assertEqual(profile.index_number, 'S12345')

    def test_student_profile_unique_index_number(self):
        user2 = User.objects.create_user(username='student2', password='pwd')

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                 StudentProfile.objects.create(user=user2, index_number='S12345')

        user3 = User.objects.create_user(username='student3', password='pwd')
        profile3 = StudentProfile.objects.create(user=user3, index_number='S98765')
        self.assertEqual(profile3.index_number, 'S98765')

    def test_access_user_from_student_profile(self):
        profile = StudentProfile.objects.get(index_number='S12345')
        self.assertEqual(profile.user.username, 'student_user')

    def test_access_student_profile_from_user(self):
        user = User.objects.get(username='student_user')
        profile = user.studentprofile
        self.assertEqual(profile.index_number, 'S12345')

    def test_access_nonexistent_student_profile_from_user(self):
        user_without_profile = User.objects.create_user(username='nouserprofile', password='pwd')
        with self.assertRaises(StudentProfile.DoesNotExist):
            user_without_profile.studentprofile

    def test_onetoone_cascade_delete_student_profile(self):
        user_to_delete = User.objects.create_user(username='user_del_sp', password='pwd')
        profile_to_delete = StudentProfile.objects.create(user=user_to_delete, index_number='S00001')

        user_id = user_to_delete.id
        profile_user_id = profile_to_delete.user_id

        self.assertEqual(User.objects.filter(id=user_id).count(), 1)
        self.assertEqual(StudentProfile.objects.filter(user_id=profile_user_id).count(), 1)


        user_to_delete.delete()

        self.assertEqual(User.objects.filter(id=user_id).count(), 0)
        self.assertEqual(StudentProfile.objects.filter(user_id=profile_user_id).count(), 0)

    def test_student_profile_str_representation(self):
        profile = StudentProfile.objects.get(user=self.student_user)
        self.assertEqual(str(profile), f'Profil studenta: {self.student_user.username} ({self.student_profile.index_number})')

class SupervisorProfileModelTests(BaseModelTests):
    def test_supervisor_profile_creation(self):
        self.assertEqual(SupervisorProfile.objects.count(), 1)
        profile = SupervisorProfile.objects.get(user=self.supervisor_user)
        self.assertEqual(profile.bacherol_limit, 1)
        self.assertEqual(profile.engineering_limit, 1)
        self.assertEqual(profile.master_limit, 1)
        self.assertEqual(profile.phd_limit, 1)

        user2 = User.objects.create_user(username='sup2', password='pwd')
        sup_profile2 = SupervisorProfile.objects.create(user=user2, master_limit=10, phd_limit=5)
        self.assertEqual(sup_profile2.bacherol_limit, 1)
        self.assertEqual(sup_profile2.engineering_limit, 1)
        self.assertEqual(sup_profile2.master_limit, 10)
        self.assertEqual(sup_profile2.phd_limit, 5)

    def test_access_user_from_supervisor_profile(self):
        profile = SupervisorProfile.objects.get(user=self.supervisor_user)
        self.assertEqual(profile.user.username, 'supervisor_user')

    def test_access_supervisor_profile_from_user(self):
        user = User.objects.get(username='supervisor_user')
        profile = user.supervisorprofile
        self.assertEqual(profile.user.username, 'supervisor_user')


    def test_access_nonexistent_supervisor_profile_from_user(self):
        user_without_profile = User.objects.create_user(username='no_sup_profile', password='pwd')
        with self.assertRaises(SupervisorProfile.DoesNotExist):
            user_without_profile.supervisorprofile


    def test_onetoone_cascade_delete_supervisor_profile(self):
        user_to_delete = User.objects.create_user(username='user_del_sup', password='pwd')
        profile_to_delete = SupervisorProfile.objects.create(user=user_to_delete, master_limit=7)

        user_id = user_to_delete.id
        profile_user_id = profile_to_delete.user_id

        self.assertEqual(User.objects.filter(id=user_id).count(), 1)
        self.assertEqual(SupervisorProfile.objects.filter(user_id=profile_user_id).count(), 1)


        user_to_delete.delete()

        self.assertEqual(User.objects.filter(id=user_id).count(), 0)
        self.assertEqual(SupervisorProfile.objects.filter(user_id=profile_user_id).count(), 0)


    def test_supervisor_profile_str_representation(self):
        profile = SupervisorProfile.objects.get(user=self.supervisor_user)
        self.assertEqual(str(profile), f'{self.supervisor_user.academic_title} {self.supervisor_user.username}')

        user_no_title_sup = User.objects.create_user(username='notitle_sup', password='pwd', academic_title=AcademicTitle.NONE)
        profile_no_title_sup = SupervisorProfile.objects.create(user=user_no_title_sup)
        self.assertEqual(str(profile_no_title_sup), f'{AcademicTitle.NONE} {user_no_title_sup.username}')


class LogsModelTests(BaseModelTests):
    def test_log_creation_with_user(self):
        log = Logs.objects.create(
            user_id=self.basic_user,
            description="User logged in."
        )
        self.assertEqual(Logs.objects.count(), 1)
        self.assertEqual(log.user_id, self.basic_user)
        self.assertEqual(log.description, "User logged in.")
        self.assertIsNotNone(log.timestamp)
        self.assertAlmostEqual(log.timestamp, timezone.now(), delta=timezone.timedelta(seconds=1))

    def test_log_creation_without_user(self):
        log = Logs.objects.create(
            description="System startup."
        )
        self.assertEqual(Logs.objects.count(), 1)
        self.assertIsNone(log.user_id)
        self.assertEqual(log.description, "System startup.")
        self.assertIsNotNone(log.timestamp)
        self.assertAlmostEqual(log.timestamp, timezone.now(), delta=timezone.timedelta(seconds=1))

    def test_log_creation_empty_description(self):
        log = Logs.objects.create(
            user_id=self.basic_user,
            description=""
        )
        self.assertEqual(log.description, "")
        self.assertIsNotNone(log.description)

    def test_log_creation_null_description(self):
        log = Logs.objects.create(
            user_id=self.basic_user,
            description=None
        )
        self.assertIsNone(log.description)

    def test_log_user_on_delete_set_null(self):
        user_to_delete = User.objects.create_user(username='temp_user_for_log_del', password='pwd')
        log = Logs.objects.create(user_id=user_to_delete, description="Action by temp user.")
        log_id = log.id
        user_id_before_delete = user_to_delete.id

        self.assertIsNotNone(log.user_id)

        user_to_delete.delete()

        retrieved_log = Logs.objects.get(id=log_id)

        self.assertIsNone(retrieved_log.user_id)

        with self.assertRaises(User.DoesNotExist):
             User.objects.get(id=user_id_before_delete)

    def test_log_str_representation(self):
        log_with_user = Logs.objects.create(
            user_id=self.student_user,
            description="Short desc."
        )
        log_without_user = Logs.objects.create(
            description="Another desc."
        )
        long_desc = "a" * 100
        log_long_desc = Logs.objects.create(description=long_desc)

        expected_str_with_user_prefix = f"Zmiana {log_with_user.id} ("
        self.assertTrue(str(log_with_user).startswith(expected_str_with_user_prefix))
        self.assertIn(f"zrobiona przez {self.student_user.username}", str(log_with_user))
        self.assertIn("Short desc.", str(log_with_user))

        expected_str_without_user_prefix = f"Zmiana {log_without_user.id} ("
        self.assertTrue(str(log_without_user).startswith(expected_str_without_user_prefix))
        self.assertIn("zrobiona przez Brak użytkownika", str(log_without_user))
        self.assertIn("Another desc.", str(log_without_user))

        self.assertIn(long_desc[:50], str(log_long_desc))
        self.assertIn("...", str(log_long_desc))