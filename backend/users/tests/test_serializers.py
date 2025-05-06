from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIRequestFactory 
from common.models import Department, Tag
from users.models import *
from users.serializers.user_list_serializer import UserListSerializer
from users.serializers.user_serializer import UserSerializer
from users.serializers.student_serializer import StudentProfileSerializer
from users.serializers.supervisor_serializer import SupervisorProfileSerializer
from django.db import transaction
from users.serializers.user_tags_serializer import TagsUpdateSerializer
from users.serializers.single_user_create_serializer import SingleUserCreateSerializer

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

class UserListSerializerTests(APITestCase):

    def setUp(self):
        factory = APIRequestFactory()
        self.request = factory.get('/')

        self.department_it = Department.objects.create(name="Wydział IT", description="Opis IT")

        self.user_promotor = User.objects.create_user(
            username='promotor_list',
            password='password',
            email='promotor_list@example.com',
            first_name='Adam',
            last_name='Promotor',
            academic_title=AcademicTitle.DOCTOR,
            role=Role.SUPERVISOR,
            description='Opis promotora',
            department=self.department_it
        )

        self.user_student = User.objects.create_user(
            username='student_list',
            password='password',
            email='student_list@example.com',
            first_name='Ewa',
            last_name='Studentka',
            academic_title=AcademicTitle.NONE,
            role=Role.STUDENT,
            description='Opis studentki',
            department=self.department_it
        )


    def test_serialization_of_user_list(self):
        users = User.objects.filter(username__in=['promotor_list', 'student_list'])
        serializer = UserListSerializer(users, many=True, context={'request': self.request}) 
        data = serializer.data

        self.assertEqual(len(data), 2)

        user1_data = next((item for item in data if item['email'] == 'promotor_list@example.com'), None)
        self.assertIsNotNone(user1_data)
        self.assertIn('url', user1_data)
        self.assertIsNotNone(user1_data['url']) 
        self.assertEqual(user1_data['academic_title'], AcademicTitle.DOCTOR)
        self.assertEqual(user1_data['first_name'], 'Adam')
        self.assertEqual(user1_data['last_name'], 'Promotor')
        self.assertEqual(user1_data['email'], 'promotor_list@example.com')
        self.assertEqual(user1_data['role'], Role.SUPERVISOR)

        user2_data = next((item for item in data if item['email'] == 'student_list@example.com'), None)
        self.assertIsNotNone(user2_data)
        self.assertIn('url', user2_data)
        self.assertIsNotNone(user2_data['url'])
        self.assertEqual(user2_data['academic_title'], AcademicTitle.NONE)
        self.assertEqual(user2_data['first_name'], 'Ewa')
        self.assertEqual(user2_data['last_name'], 'Studentka')
        self.assertEqual(user2_data['email'], 'student_list@example.com')
        self.assertEqual(user2_data['role'], Role.STUDENT)

    def test_user_list_serializer_read_only_fields(self):
        user = User.objects.create_user(username='test_ro', password='pw', email='ro@example.com', role=Role.STUDENT)
        data = {
            'username': 'new_username', 
            'first_name': 'Nowe Imie', 
            'role': Role.SUPERVISOR 
        }
        serializer = UserListSerializer(instance=user, data=data, partial=True) 
        
        self.assertTrue(serializer.is_valid(), serializer.errors) 

        self.assertNotIn('username', serializer.validated_data)
        self.assertNotIn('first_name', serializer.validated_data)
        self.assertNotIn('role', serializer.validated_data)


class TagsUpdateSerializerTests(APITestCase):

    def setUp(self):
        self.tag_python = Tag.objects.create(name="Python")
        self.tag_django = Tag.objects.create(name="Django")
        self.tag_rest = Tag.objects.create(name="REST API")
        self.tag_db = Tag.objects.create(name="Bazy Danych")


    def test_valid_data_adds_tags(self):
        data = {'to_add': [self.tag_python.id, self.tag_django.id]}
        serializer = TagsUpdateSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        self.assertIn('to_add', serializer.validated_data)
        self.assertListEqual(
            sorted(serializer.validated_data['to_add'], key=lambda t: t.id),
            sorted([self.tag_python, self.tag_django], key=lambda t: t.id)
        )
        self.assertNotIn('to_remove', serializer.validated_data)


    def test_valid_data_removes_tags(self):
        data = {'to_remove': [self.tag_rest.id, self.tag_db.id]}
        serializer = TagsUpdateSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertIn('to_remove', serializer.validated_data)
        self.assertListEqual(
            sorted(serializer.validated_data['to_remove'], key=lambda t: t.id),
            sorted([self.tag_rest, self.tag_db], key=lambda t: t.id)
        )
        self.assertNotIn('to_add', serializer.validated_data)


    def test_valid_data_adds_and_removes_tags(self):
        data = {
            'to_add': [self.tag_python.id, self.tag_rest.id],
            'to_remove': [self.tag_django.id, self.tag_db.id]
        }
        serializer = TagsUpdateSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertIn('to_add', serializer.validated_data)
        self.assertListEqual(
            sorted(serializer.validated_data['to_add'], key=lambda t: t.id),
            sorted([self.tag_python, self.tag_rest], key=lambda t: t.id)
        )

        self.assertIn('to_remove', serializer.validated_data)
        self.assertListEqual(
            sorted(serializer.validated_data['to_remove'], key=lambda t: t.id),
            sorted([self.tag_django, self.tag_db], key=lambda t: t.id)
        )


    def test_empty_lists_are_valid(self):
        data = {'to_add': [], 'to_remove': []}
        serializer = TagsUpdateSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertIn('to_add', serializer.validated_data)
        self.assertEqual(serializer.validated_data['to_add'], [])
        self.assertIn('to_remove', serializer.validated_data)
        self.assertEqual(serializer.validated_data['to_remove'], [])

    def test_missing_fields_are_valid(self):
        data1 = {'to_add': [self.tag_python.id]}
        serializer1 = TagsUpdateSerializer(data=data1)
        self.assertTrue(serializer1.is_valid(), serializer1.errors)
        self.assertIn('to_add', serializer1.validated_data)
        self.assertNotIn('to_remove', serializer1.validated_data) 

        data2 = {'to_remove': [self.tag_django.id]}
        serializer2 = TagsUpdateSerializer(data=data2)
        self.assertTrue(serializer2.is_valid(), serializer2.errors)
        self.assertNotIn('to_add', serializer2.validated_data)
        self.assertIn('to_remove', serializer2.validated_data)

        data3 = {}
        serializer3 = TagsUpdateSerializer(data=data3)
        self.assertTrue(serializer3.is_valid(), serializer3.errors)
        self.assertNotIn('to_add', serializer3.validated_data)
        self.assertNotIn('to_remove', serializer3.validated_data)


    def test_invalid_tag_id_in_to_add(self):
        data = {'to_add': [self.tag_python.id, 999]} 
        serializer = TagsUpdateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('to_add', serializer.errors) 
        self.assertIn('Invalid pk "999" - object does not exist.', str(serializer.errors['to_add']))


    def test_invalid_tag_id_in_to_remove(self):
        data = {'to_remove': [self.tag_rest.id, 888]} 
        serializer = TagsUpdateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('to_remove', serializer.errors)
        self.assertIn('Invalid pk "888" - object does not exist.', str(serializer.errors['to_remove']))

    def test_non_list_input_for_fields(self):
        data1 = {'to_add': self.tag_python.id} 
        serializer1 = TagsUpdateSerializer(data=data1)
        self.assertFalse(serializer1.is_valid())
        self.assertIn('to_add', serializer1.errors)
        self.assertIn('Expected a list of items but got type "int".', str(serializer1.errors['to_add']))

        data2 = {'to_remove': "invalid"} 
        serializer2 = TagsUpdateSerializer(data=data2)
        self.assertFalse(serializer2.is_valid())
        self.assertIn('to_remove', serializer2.errors)
        self.assertIn('Expected a list of items but got type "str".', str(serializer2.errors['to_remove']))

