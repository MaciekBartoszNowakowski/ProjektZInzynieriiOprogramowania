from django.test import TestCase
from django.db.utils import IntegrityError, DataError
from common.models import Department, Tag
from django.db import transaction

class DepartmentModelTests(TestCase):
    def test_department_creation(self):
        department = Department.objects.create(
            name="Wydział Testowy",
            description="Opis testowego wydziału"
        )
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(department.name, "Wydział Testowy")
        self.assertEqual(department.description, "Opis testowego wydziału")

    def test_department_str_representation(self):
        department = Department.objects.create(
            name="Wydział IT",
            description="Wydział Informatyki i Technik Informacyjnych"
        )
        expected_str = f"Wydział: {department.name} \nOpis: {department.description}"
        self.assertEqual(str(department), expected_str)

    def test_department_name_max_length(self):
        long_name = "a" * 101
        with self.assertRaises(Exception):
             Department.objects.create(name=long_name, description="Krótki opis")
             
             
class TagModelTests(TestCase):
    def test_tag_creation(self):
        """
        Test that a Tag object can be created successfully.
        """
        tag = Tag.objects.create(
            name="Test Tag"
        )
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(tag.name, "Test Tag")

    def test_tag_str_representation(self):
        tag = Tag.objects.create(
            name="Programming"
        )
        self.assertEqual(str(tag), "Programming")

    def test_tag_name_max_length(self):
        long_name = "a" * 101
        with self.assertRaises((IntegrityError, DataError)):
            with transaction.atomic():
                 Tag.objects.create(name=long_name)