#!/usr/bin/python3
"""Defines unittests for console.py.
"""
import unittest
from unittest.mock import patch
from io import StringIO
import os
from models.engine.file_storage import FileStorage
from console import HBNBCommand


class HBNBCommandTestCase(unittest.TestCase):
    """Unittests for testing prompting of the HBNB command interpreter"""
    @classmethod
    def setUp(self):
        self.console = HBNBCommand()
        try:
            os.rename('file.json', 'tmp')
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove('file.json')
        except IOError:
            pass
        try:
            os.rename('tmp', 'file.json')
        except IOError:
            pass

    def test_prompt(self):
        self.assertEqual(self.console.prompt, '(hbnb) ')

    def test_quit(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertTrue(self.console.onecmd('quit'))
            self.assertEqual(output.getvalue().strip(), '')

    def test_help_quit(self):
        message = 'Quit command to exit the program'
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertFalse(self.console.onecmd('help quit'))

    def test_EOF(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertTrue(self.console.onecmd('EOF'))
            self.assertEqual(output.getvalue(), '\n')

    def test_help_EOF(self):
        message = "EOF signal to exit the program"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(self.console.onecmd('help EOF'))

    def test_emptyline(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertFalse(self.console.onecmd(''))
            self.assertEqual(output.getvalue(), '')


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
            # self.assertEqual(message, output.getvalue().strip)
