#!/usr/bin/python3
"""Defines unittests for console.py.
"""
import unittest
from unittest.mock import patch
from io import StringIO
import os
from models.engine.file_storage import FileStorage
from console import HBNBCommand


class HBNBCommandCreateTestCase(unittest.TestCase):
    """Unittests for testing create from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        self.console = HBNBCommand()
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_missing_class(self):
        message = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(self.console.onecmd("create"))
            self.assertEqual(message, output.getvalue().strip())

    def test_create_invalid_class(self):
        message = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(self.console.onecmd("create MyModel"))
            self.assertEqual(message, output.getvalue().strip())

    def test_invalid_syntax(self):
        message = "*** Unknown syntax: MyModel.create()"
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertFalse(self.console.onecmd('MyModel.create()'))
            # self.assertEqual(message, output.getvalue().strip())
