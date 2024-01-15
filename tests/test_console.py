#!/usr/bin/python3
'''Module for Console unit tests.'''
import unittest
from unittest.mock import patch
from io import StringIO
import os
import console
from console import HBNBCommand
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.base_model import BaseModel


class TestConsole(unittest.TestCase):
    '''Tests the HBNBCommand class.'''

    def setUp(self):
        '''Creates an instance of HBNBCommand'''
        self.console = HBNBCommand()

    def tearDown(self):
        '''Cleans up resources after tests'''
        del self.console
        # Clean up file.json after each test
        if os.path.exists("file.json"):
            os.remove("file.json")

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_create(self, mock_stdout):
        '''Test create command'''
        self.console.onecmd("create BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertIsNotNone(output)
        self.assertNotEqual("** class name missing **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_show(self, mock_stdout):
        '''T1: Test show command'''
        self.console.onecmd("show BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_destroy(self, mock_stdout):
        '''T2: Test destroy command'''
        self.console.onecmd("destroy BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)
        self.assertEqual("** instance id missing **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_all(self, mock_stdout):
        '''T3: Test all command'''
        self.console.onecmd("all BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_update(self, mock_stdout):
        '''T4: Test update command'''
        self.console.onecmd("update BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_create_with_params(self, mock_stdout):
        '''T5: Test create command with parameters'''
        self.console.onecmd("create BaseModel name=\"John\" age=25")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_show_with_params(self, mock_stdout):
        '''T6: Test show command with parameters'''
        self.console.onecmd("create BaseModel")
        id = mock_stdout.getvalue().strip()
        self.console.onecmd(f"show BaseModel {id} name")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)
        self.assertNotEqual("** instance id missing **", output)
        self.assertNotEqual("** no instance found **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_destroy_with_params(self, mock_stdout):
        '''T7: Test destroy command works'''
        self.console.onecmd("create BaseModel")
        id = mock_stdout.getvalue().strip()
        self.console.onecmd(f"destroy BaseModel {id}")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)
        self.assertNotEqual("** instance id missing **", output)
        self.assertNotEqual("** no instance found **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_all_with_params(self, mock_stdout):
        '''T8: Test all command with parameters'''
        self.console.onecmd("all BaseModel name=\"John\" age=25")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_update_with_params(self, mock_stdout):
        '''T9: Test update command with parameters'''
        self.console.onecmd("create BaseModel")
        id = mock_stdout.getvalue().strip()
        self.console.onecmd(f"update BaseModel {id} name=\"John\"")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)
        self.assertNotEqual("** instance id missing **", output)
        self.assertNotEqual("** no instance found **", output)
        self.assertNotEqual("** attribute name missing **", output)
        self.assertNotEqual("** value missing **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_update_invalid_attribute(self, mock_stdout):
        '''T10: Test update command with multiple params'''
        self.console.onecmd("create BaseModel")
        id = mock_stdout.getvalue().strip()
        cmsStr = f"update BaseModel {id}"
        cmsStr += " email \"aibnb@mail.com\" first_name \"Betty\""
        self.console.onecmd(cmsStr)
        self.console.onecmd(f"show BaseModel {id}")
        output = mock_stdout.getvalue().strip()

        self.assertIn("email", output)
        self.assertNotIn("first_name", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_update_with_different_attribute_types(self, mock_stdout):
        '''T11: Test update command with different attribute types
        [TODO] try it when you have int methods'''
        self.console.onecmd("create BaseModel")
        id = mock_stdout.getvalue().strip()
        self.console.onecmd(f"update BaseModel {id} age 25")
        self.console.onecmd(f"show BaseModel {id}")
        output = mock_stdout.getvalue().strip()

        self.assertIn("age", output)
        self.assertIn("25", output)
        self.assertIsInstance(storage.all()[f"BaseModel.{id}"].age, str)
        # self.assertIsInstance(storage.all()[f"BaseModel.{id}"].age, int)

    def test_prompt(self):
        """test the prompt"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertEqual(HBNBCommand().prompt, "(hbnb) ")

    # def test_help_messages(self):
    #     """
    #     test help messages for the commands
    #     """
    #     with patch('sys.stdout', new=StringIO()) as f:
    #         HBNBCommand().onecmd("help quit")
    #         self.assertEqual(
    #             "Quit command to exit the program\n\n", f.getvalue())

    #     with patch('sys.stdout', new=StringIO()) as f:
    #         HBNBCommand().onecmd("help EOF")
    #         self.assertEqual(
    #             "A clean way to exit interpreter\n\n", f.getvalue())

    def test_emptyline(self):
        """test the empty line and enter command"""

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("")
            self.assertEqual("", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
            self.assertEqual("", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("random command")
            self.assertEqual("*** Unknown syntax: random command\n",
                             f.getvalue())

    # def test_quit(self):
    #     """test quit command"""
    #     with patch('sys.stdout', new=StringIO()) as f:
    #         HBNBCommand().onecmd("quit")
    #         self.assertEqual("", f.getvalue())

    # def test_EOF(self):
    #     """test EOF command"""
    #     with patch('sys.stdout', new=StringIO()) as f:
    #         HBNBCommand().onecmd("EOF")
    #         self.assertEqual("\n", f.getvalue())

    def test_create(self):
        """test create function"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual("** class name missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Mahmoud")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            self.assertNotEqual(f.getvalue(), '')

    def test_show(self):
        """test all function"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            self.assertEqual("** class name missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Mahmoud")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show User 123")
            self.assertEqual("** no instance found **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            u = User()
            storage.new(u)
            storage.save()
            cmd = f"show User {u.id}"
            HBNBCommand().onecmd(cmd)
            self.assertNotEqual(f.getvalue(), '')

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"User.show(\"{u.id}\")")
            self.assertNotEqual(f.getvalue(), '')

    def test_all(self):
        """test all function"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all Mahmoud")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
            self.assertNotEqual(f.getvalue(), '')

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all User")
        self.assertNotEqual(f.getvalue(), '')

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("City.all()")
        self.assertNotEqual(f.getvalue(), '')

    def test_destroy(self):
        """test destroy function"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            self.assertEqual("** class name missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy Sara")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy User")
            self.assertEqual("** instance id missing **\n", f.getvalue())

        u = User()
        storage.new(u)
        storage.save()
        # with patch('sys.stdout', new=StringIO()) as f:
        #     HBNBCommand().onecmd(f"User.destroy(\"{u.id}\")")
        #     self.assertEqual("", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy User 123")
            self.assertEqual("** no instance found **\n", f.getvalue())

    def test_update(self):
        """test update function"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
            self.assertEqual("** class name missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update Sara")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User 123")
            self.assertEqual("** no instance found **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            b = BaseModel()
            cmd = f"update BaseModel {b.id}"
            HBNBCommand().onecmd(cmd)
            self.assertEqual("** attribute name missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            cmd = f"update BaseModel {b.id} first_name"
            HBNBCommand().onecmd(cmd)
            self.assertEqual("** value missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            cmd = f"update BaseModel {b.id} first_name \"TutTrueee\""
            HBNBCommand().onecmd(cmd)
            self.assertEqual("", f.getvalue())

        # with patch('sys.stdout', new=StringIO()) as f:
        #     cmd = f"BaseModel.update(\"{b.id}\",\"first_name\",\"TutTrueee\")"
        #     HBNBCommand().onecmd(cmd)
        #     self.assertEqual("", f.getvalue())

    def test_count(self):
        """test the count function"""
        with patch('sys.stdout', new=StringIO()) as f:
            u = User()
            storage.new(u)
            storage.save()
            HBNBCommand().onecmd("User.count()")
            self.assertNotEqual(0, f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("invalid.count()")
            self.assertEqual("*** Unknown syntax: invalid.count()\n",
                             f.getvalue())

    def test_docstrings(self):
        """ test doc string for console module"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand().do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand().do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand().emptyline.__doc__)
        # self.assertIsNotNone(HBNBCommand().do_create.__doc__)
        self.assertIsNotNone(HBNBCommand().do_all.__doc__)
        self.assertIsNotNone(HBNBCommand().do_show.__doc__)
        self.assertIsNotNone(HBNBCommand().do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand().do_update.__doc__)
        self.assertIsNotNone(HBNBCommand().default.__doc__)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_create_with_params_new_feature(self, mock_stdout):
        '''Test create command with parameters (new feature)'''
        self.console.onecmd("create InvalidClass invalid_param=\"invalid_value\"")
        output = mock_stdout.getvalue().strip()
        self.assertEqual("** class doesn't exist **", output)

        self.console.onecmd("create State name=\"California\"")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)

        self.console.onecmd("create Place city_id=\"0001\" user_id=\"0001\" name=\"My_little_house\" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)



if __name__ == '__main__':
    unittest.main()
