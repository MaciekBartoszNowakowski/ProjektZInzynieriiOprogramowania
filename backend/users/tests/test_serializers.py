from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from common.models import Department, Tag
from users.models import *
from users.serializers.user_serializer import UserSerializer
from users.serializers.student_serializer import StudentProfileSerializer
from users.serializers.supervisor_serializer import SupervisorProfileSerializer
from django.db import transaction

User = get_user_model()

class UserSerializerTests(APITestCase):

    def setUp(self):
        self.department_it = Department.objects.create(name="Wydział IT", description="Opis IT")
        self.tag_python = Tag.objects.create(name="Python")
        self.tag_django = Tag.objects.create(name="Django")
        self.tag_rest = Tag.objects.create(name="REST API")

        self.user_with_tags = User.objects.create_user(
            username='user_tags',
            password='password',
            email='user_tags@example.com',
            first_name='Jan',
            last_name='Kowalski',
            academic_title=AcademicTitle.DOCTOR,
            role=Role.SUPERVISOR,
            description='Opis użytkownika z tagami',
            department=self.department_it
        )
        self.user_with_tags.tags.add(self.tag_python, self.tag_django)

        self.user_without_tags = User.objects.create_user(
            username='user_no_tags',
            password='password',
            email='user_no_tags@example.com',
            first_name='Anna',
            last_name='Nowak',
            academic_title=AcademicTitle.NONE,
            role=Role.STUDENT,
            description='Opis użytkownika bez tagów',
            department=self.department_it
        )

    def test_serializer_contains_expected_fields(self):
        serializer = UserSerializer(instance=self.user_with_tags)
        data = serializer.data

        expected_fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'academic_title',
            'role',
            'description',
            'department',
            'tags'
        ]
        self.assertEqual(set(data.keys()), set(expected_fields))

    def test_serializer_data_for_user_with_tags(self):
        serializer = UserSerializer(instance=self.user_with_tags)
        data = serializer.data

        self.assertEqual(data['id'], self.user_with_tags.id)
        self.assertEqual(data['username'], 'user_tags')
        self.assertEqual(data['email'], 'user_tags@example.com')
        self.assertEqual(data['first_name'], 'Jan')
        self.assertEqual(data['last_name'], 'Kowalski')
        self.assertEqual(data['academic_title'], AcademicTitle.DOCTOR)
        self.assertEqual(data['role'], Role.SUPERVISOR)
        self.assertEqual(data['description'], 'Opis użytkownika z tagami')
        self.assertEqual(data['department'], self.department_it.id)

        expected_tags = [self.tag_python.name, self.tag_django.name]
        self.assertListEqual(sorted(data['tags']), sorted(expected_tags))

    def test_serializer_data_for_user_without_tags(self):
        serializer = UserSerializer(instance=self.user_without_tags)
        data = serializer.data

        self.assertEqual(data['id'], self.user_without_tags.id)
        self.assertEqual(data['username'], 'user_no_tags')
        self.assertEqual(data['email'], 'user_no_tags@example.com')
        self.assertEqual(data['first_name'], 'Anna')
        self.assertEqual(data['last_name'], 'Nowak')
        self.assertEqual(data['academic_title'], AcademicTitle.NONE)
        self.assertEqual(data['role'], Role.STUDENT)
        self.assertEqual(data['description'], 'Opis użytkownika bez tagów')
        self.assertEqual(data['department'], self.department_it.id)

        self.assertListEqual(data['tags'], [])

    def test_deserialization_ignores_read_only_fields_and_validates_writable(self):
        data = {
            'username': 'new_username',
            'first_name': 'Nowe Imię',
            'description': 'Nowy opis',
            'tags': ['NowyTag']
        }

        serializer = UserSerializer(instance=self.user_with_tags, data=data, partial=True)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertEqual(serializer.validated_data.get('description'), 'Nowy opis')
        self.assertNotIn('username', serializer.validated_data)
        self.assertNotIn('first_name', serializer.validated_data)
        self.assertNotIn('academic_title', serializer.validated_data)
        self.assertNotIn('role', serializer.validated_data)
        self.assertNotIn('department', serializer.validated_data)
        self.assertNotIn('tags', serializer.validated_data)


class StudentProfileSerializerTests(APITestCase):

    def setUp(self):
        self.department_it = Department.objects.create(name="Wydział IT", description="Opis IT")
        self.tag_python = Tag.objects.create(name="Python")
        self.tag_django = Tag.objects.create(name="Django")

        self.user_student = User.objects.create_user(
            username='student_user_test',
            password='password123',
            email='student.test@example.com',
            first_name='Test',
            last_name='Student',
            academic_title=AcademicTitle.NONE,
            role=Role.STUDENT,
            description='Initial student description',
            department=self.department_it
        )
        self.user_student.tags.add(self.tag_python)

        self.student_profile = StudentProfile.objects.create(
            user=self.user_student,
            index_number='S98765'
        )

        self.user_student_update = User.objects.create_user(
            username='student_update_test',
            password='password123',
            email='student.update@example.com',
            first_name='Update',
            last_name='Student',
            academic_title=AcademicTitle.BACHELOR,
            role=Role.STUDENT,
            description='Description before update',
            department=self.department_it
        )
        self.student_profile_update = StudentProfile.objects.create(
            user=self.user_student_update,
            index_number='S11223'
        )


    def test_serializer_contains_expected_fields(self):
        serializer = StudentProfileSerializer(instance=self.student_profile)
        data = serializer.data

        expected_fields = ['user', 'index_number']
        self.assertEqual(set(data.keys()), set(expected_fields))

    def test_serializer_data_serialization(self):
        serializer = StudentProfileSerializer(instance=self.student_profile)
        data = serializer.data

        self.assertEqual(data['index_number'], 'S98765')

        self.assertIn('user', data)
        user_data = data['user']

        self.assertEqual(user_data['id'], self.user_student.id)
        self.assertEqual(user_data['username'], 'student_user_test')
        self.assertEqual(user_data['email'], 'student.test@example.com')
        self.assertEqual(user_data['first_name'], 'Test')
        self.assertEqual(user_data['last_name'], 'Student')
        self.assertEqual(user_data['academic_title'], AcademicTitle.NONE)
        self.assertEqual(user_data['role'], Role.STUDENT)
        self.assertEqual(user_data['description'], 'Initial student description')
        self.assertEqual(user_data['department'], self.department_it.id)

        expected_tags = [self.tag_python.name]
        self.assertListEqual(sorted(user_data['tags']), sorted(expected_tags))


    def test_deserialization_validates_nested_user_description(self):
        new_description = 'Updated description via nested data'
        data = {'user': {'description': new_description}}

        serializer = StudentProfileSerializer(
            instance=self.student_profile_update,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertIn('user', serializer.validated_data)
        self.assertEqual(serializer.validated_data['user'].get('description'), new_description)
        self.assertNotIn('index_number', serializer.validated_data)


    def test_deserialization_ignores_other_nested_user_fields(self):
        data = {
            'user': {
                'username': 'new_username',
                'first_name': 'New First Name',
                'academic_title': AcademicTitle.PROFESSOR,
                'role': Role.ADMIN,
                'department': self.department_it.id,
                'tags': ['NewTag'],
                'description': 'Description that should be updated'
            }
        }

        serializer = StudentProfileSerializer(
            instance=self.student_profile_update,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertIn('user', serializer.validated_data)
        user_data = serializer.validated_data['user']
        self.assertEqual(user_data.get('description'), 'Description that should be updated')

        self.assertNotIn('username', user_data)
        self.assertNotIn('first_name', user_data)
        self.assertNotIn('academic_title', user_data)
        self.assertNotIn('role', user_data)
        self.assertNotIn('department', user_data)
        self.assertNotIn('tags', user_data)

        self.assertNotIn('index_number', serializer.validated_data)


    def test_deserialization_ignores_profile_fields(self):
        data = {
            'index_number': 'S99999',
            'user': {
                 'description': 'Description updated via profile field test'
            }
        }

        serializer = StudentProfileSerializer(
            instance=self.student_profile_update,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertIn('user', serializer.validated_data)
        self.assertEqual(serializer.validated_data['user'].get('description'), 'Description updated via profile field test')

        self.assertNotIn('index_number', serializer.validated_data)


    def test_deserialization_with_null_description_via_nested_user_data(self):
        data_empty = {'user': {'description': ''}}
        serializer_empty = StudentProfileSerializer(
            instance=self.student_profile_update,
            data=data_empty,
            partial=True
        )
        self.assertTrue(serializer_empty.is_valid(), serializer_empty.errors)
        self.assertIn('user', serializer_empty.validated_data)
        self.assertEqual(serializer_empty.validated_data['user'].get('description'), '')

        data_null = {'user': {'description': None}}
        serializer_null = StudentProfileSerializer(
            instance=self.student_profile_update,
            data=data_null,
            partial=True
        )
        self.assertTrue(serializer_null.is_valid(), serializer_null.errors)
        self.assertIn('user', serializer_null.validated_data)
        self.assertIsNone(serializer_null.validated_data['user'].get('description'))


    def test_deserialization_without_user_data(self):
        data = {}

        serializer = StudentProfileSerializer(
            instance=self.student_profile_update,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertNotIn('user', serializer.validated_data)
        self.assertNotIn('index_number', serializer.validated_data)


class SupervisorProfileSerializerTests(APITestCase):

    def setUp(self):
        self.department_el = Department.objects.create(name="Wydział EL", description="Opis EL")
        self.tag_ai = Tag.objects.create(name="AI")
        self.tag_ml = Tag.objects.create(name="ML")

        self.user_supervisor = User.objects.create_user(
            username='supervisor_user_test',
            password='password123',
            email='supervisor.test@example.com',
            first_name='Test',
            last_name='Supervisor',
            academic_title=AcademicTitle.PROFESSOR,
            role=Role.SUPERVISOR,
            description='Initial supervisor description',
            department=self.department_el
        )
        self.user_supervisor.tags.add(self.tag_ai, self.tag_ml)

        self.supervisor_profile = SupervisorProfile.objects.create(
            user=self.user_supervisor,
            bacherol_limit=5,
            engineering_limit=7,
            master_limit=10,
            phd_limit=3
        )

        self.user_supervisor_update = User.objects.create_user(
            username='supervisor_update_test',
            password='password123',
            email='supervisor.update@example.com',
            first_name='Update',
            last_name='Supervisor',
            academic_title=AcademicTitle.DOCTOR,
            role=Role.SUPERVISOR,
            description='Description before update',
            department=self.department_el
        )
        self.supervisor_profile_update = SupervisorProfile.objects.create(
            user=self.user_supervisor_update,
            bacherol_limit=1,
            engineering_limit=1,
            master_limit=1,
            phd_limit=1
        )


    def test_serializer_contains_expected_fields(self):
        serializer = SupervisorProfileSerializer(instance=self.supervisor_profile)
        data = serializer.data

        expected_fields = [
            'user',
            'bacherol_limit',
            'engineering_limit',
            'master_limit',
            'phd_limit'
        ]
        self.assertEqual(set(data.keys()), set(expected_fields))


    def test_serializer_data_serialization(self):
        serializer = SupervisorProfileSerializer(instance=self.supervisor_profile)
        data = serializer.data

        self.assertEqual(data['bacherol_limit'], 5)
        self.assertEqual(data['engineering_limit'], 7)
        self.assertEqual(data['master_limit'], 10)
        self.assertEqual(data['phd_limit'], 3)

        self.assertIn('user', data)
        user_data = data['user']

        self.assertEqual(user_data['id'], self.user_supervisor.id)
        self.assertEqual(user_data['username'], 'supervisor_user_test')
        self.assertEqual(user_data['email'], 'supervisor.test@example.com')
        self.assertEqual(user_data['first_name'], 'Test')
        self.assertEqual(user_data['last_name'], 'Supervisor')
        self.assertEqual(user_data['academic_title'], AcademicTitle.PROFESSOR)
        self.assertEqual(user_data['role'], Role.SUPERVISOR)
        self.assertEqual(user_data['description'], 'Initial supervisor description')
        self.assertEqual(user_data['department'], self.department_el.id)

        expected_tags = [self.tag_ai.name, self.tag_ml.name]
        self.assertListEqual(sorted(user_data['tags']), sorted(expected_tags))


    def test_deserialization_validates_nested_user_description(self):
        new_description = 'Updated supervisor description via nested data'
        data = {'user': {'description': new_description}}

        serializer = SupervisorProfileSerializer(
            instance=self.supervisor_profile_update,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertIn('user', serializer.validated_data)
        self.assertEqual(serializer.validated_data['user'].get('description'), new_description)


    def test_deserialization_validates_limits(self):
        new_data = {
            'bacherol_limit': 10,
            'master_limit': 15,
        }

        serializer = SupervisorProfileSerializer(
            instance=self.supervisor_profile_update,
            data=new_data,
            partial=True
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertEqual(serializer.validated_data.get('bacherol_limit'), 10)
        self.assertEqual(serializer.validated_data.get('master_limit'), 15)
        self.assertNotIn('engineering_limit', serializer.validated_data)
        self.assertNotIn('phd_limit', serializer.validated_data)
        self.assertNotIn('user', serializer.validated_data)


    def test_deserialization_validates_user_description_and_limits_together(self):
        new_description = 'Combined update description'
        new_limits_data = {
            'bacherol_limit': 12,
            'phd_limit': 4,
            'user': {'description': new_description}
        }

        serializer = SupervisorProfileSerializer(
            instance=self.supervisor_profile_update,
            data=new_limits_data,
            partial=True
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertEqual(serializer.validated_data.get('bacherol_limit'), 12)
        self.assertEqual(serializer.validated_data.get('phd_limit'), 4)
        self.assertNotIn('engineering_limit', serializer.validated_data)
        self.assertNotIn('master_limit', serializer.validated_data)

        self.assertIn('user', serializer.validated_data)
        self.assertEqual(serializer.validated_data['user'].get('description'), new_description)


    def test_deserialization_ignores_other_nested_user_fields(self):
        data = {
            'bacherol_limit': 8,
            'user': {
                'username': 'new_sup_username',
                'first_name': 'New Sup Name',
                'academic_title': AcademicTitle.HABILITATED_DOCTOR,
                'role': Role.ADMIN,
                'department': self.department_el.id,
                'tags': ['NewTagForSup'],
                'description': 'Description that should be updated'
            }
        }

        serializer = SupervisorProfileSerializer(
            instance=self.supervisor_profile_update,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertEqual(serializer.validated_data.get('bacherol_limit'), 8)

        self.assertIn('user', serializer.validated_data)
        user_data = serializer.validated_data['user']
        self.assertEqual(user_data.get('description'), 'Description that should be updated')

        self.assertNotIn('username', user_data)
        self.assertNotIn('first_name', user_data)
        self.assertNotIn('academic_title', user_data)
        self.assertNotIn('role', user_data)
        self.assertNotIn('department', user_data)
        self.assertNotIn('tags', user_data)


    def test_deserialization_with_null_description_via_nested_user_data(self):
        data_empty = {'user': {'description': ''}}
        serializer_empty = SupervisorProfileSerializer(
            instance=self.supervisor_profile_update,
            data=data_empty,
            partial=True
        )
        self.assertTrue(serializer_empty.is_valid(), serializer_empty.errors)
        self.assertIn('user', serializer_empty.validated_data)
        self.assertEqual(serializer_empty.validated_data['user'].get('description'), '')

        data_null = {'user': {'description': None}}
        serializer_null = SupervisorProfileSerializer(
            instance=self.supervisor_profile_update,
            data=data_null,
            partial=True
        )
        self.assertTrue(serializer_null.is_valid(), serializer_null.errors)
        self.assertIn('user', serializer_null.validated_data)
        self.assertIsNone(serializer_null.validated_data['user'].get('description'))


    def test_deserialization_without_user_data(self):
        initial_description = self.user_supervisor_update.description
        data = {
            'bacherol_limit': 9,
            'master_limit': 18
        }

        serializer = SupervisorProfileSerializer(
            instance=self.supervisor_profile_update,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertEqual(serializer.validated_data.get('bacherol_limit'), 9)
        self.assertEqual(serializer.validated_data.get('master_limit'), 18)
        self.assertNotIn('user', serializer.validated_data)