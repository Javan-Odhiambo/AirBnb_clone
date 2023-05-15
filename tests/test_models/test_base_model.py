#!/usr/bin/python3
"""Contains tests for the base model class.
"""
from datetime import datetime
from time import sleep
from unittest import TestCase

from models.base_model import BaseModel
from models.base_model import storage


class BaseModelTestCase(TestCase):
    """Test case for the base model class.
    """
    def setUp(self):
        """Sets up the test case.
        """
        storage._FileStorage__file_storage = "test.json"
        self.model = BaseModel()

    def test_class_has_correct_attributes(self):
        """Test the class has the attributes and they are of the correct type.
            - id (str):
            - created_at (datetime):
            - updated_at (datetime):
        """
        getattr(self.model, 'id')
        getattr(self.model, 'created_at')
        getattr(self.model, 'updated_at')

        self.assertIsInstance(self.model.id, str)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_id_is_different_for_each_object(self):
        """Test the id attribute is set correctly and is unique.
        """
        self.model = BaseModel()
        model2 = BaseModel()

        self.assertNotEqual(self.model.id, model2.id)

    def test_string_representation_of_the_object(self):
        """Test the __str__ returns the correct representation.
        """
        string = str(self.model).split(" ")

        self.assertEqual(string[0], '[' + 'BaseModel' + ']')
        self.assertEqual(len(string[1]), 38)
        self.assertEqual(string[2][0], '{')

    '''
    def test_the_save_method(self):
        """Test the save() method.
        """
        old_updated_time = self.model.updated_at
        self.model.save()
        new_updated_time = self.model.updated_at
        self.assertNotEqual(old_updated_time, new_updated_time)
    '''

    def test_the_to_dict_method(self):
        """Test the to_dict() method.
        """
        model_dict = self.model.to_dict()

        self.assertIsInstance(model_dict, dict)
        self.assertIsNotNone(model_dict.get('__class__'))
        self.assertIsInstance(model_dict.get('__class__'), str)
        self.assertEqual(model_dict.get('__class__'), 'BaseModel')
        self.assertIsInstance(model_dict.get('created_at'), str)
        self.assertIsInstance(model_dict.get('updated_at'), str)
        self.assertIsInstance(model_dict.get('id'), str)
        self.assertEqual(model_dict.get('created_at')[4], '-')

    def test_initialization_of_object_from_non_empty_dictionary(self):
        """Test the initialization of the object from a non empty dictionary.
        """
        model_dict = {
            "id": "fc0b88fd-6df9-4bed-b8fb-849ed48ed8c8",
            "created_at": "2023-05-11T06:10:19.919328",
            "updated_at": "2023-05-11T06:10:19.919337",
            "__class__": "BaseModel"
        }

        model = BaseModel(model_dict)
        getattr(model, 'id')
        getattr(model, 'created_at')
        getattr(model, 'updated_at')

    def test_initialization_of_object_from_an_empty_dictionary(self):
        """Test the initialization of the object from an empty dictionary.
        """
        model_dict = {}

        model = BaseModel(model_dict)
        getattr(model, 'id')
        getattr(model, 'created_at')
        getattr(model, 'updated_at')
