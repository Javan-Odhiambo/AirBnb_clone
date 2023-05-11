"""Contains tests for the base model class.
"""
import os
from unittest import TestCase

from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class FileStorageTestCase(TestCase):
    """Test case for the FileStorage class.
    """
    def setUp(self):
        """Sets up the test case.
        """
        self.storage = FileStorage()
        self.storage._FileStorage__objects = {}

    def gen_test_data(self):
        """Creates test objects to be used for a test
        """
        for i in range(7):
            obj = BaseModel()
            self.storage.new(obj)

    def test_class_has_correct_attributes(self):
        """Test the class has the attributes and they are of the correct type.
            - __file_path: (str)
            - __objects: (dict)
        """
        getattr(self.storage, '_FileStorage__file_path')
        getattr(self.storage, '_FileStorage__objects')

        self.assertIsInstance(self.storage._FileStorage__file_path, str)
        self.assertIsInstance(self.storage._FileStorage__objects, dict)

    def test_all_method(self):
        """Test the all() method.
        """
        self.assertAlmostEqual(self.storage.all(), {})

    def test_new_method(self):
        """Test the new() method.
        """
        self.gen_test_data()
        self.assertEqual(len(self.storage._FileStorage__objects), 7)

    def test_save_method(self):
        """Test the save() method.

            Task:
                - Add assert statements
        """
        self.gen_test_data()
        self.storage.save()

    def test_reload_method_with_non_existent_file(self):
        """Test the reload() method with a non existent file.
        """
        self.storage.reload()
        self.assertEqual(self.storage._FileStorage__objects, {})

    def test_reload_method_with_existing_file(self):
        """Test the reload() method with a existing file.
        """
        self.gen_test_data()
        self.storage.save()

        self.storage.reload()
        self.assertNotEqual(self.storage._FileStorage__objects, {})

    def tearDown(self) -> None:
        try:
            with open(self.storage._FileStorage__file_path, 'r') as f:
                pass
            os.remove(self.storage._FileStorage__file_path)
        except FileNotFoundError:
            pass

        return super().tearDown()
