#!/usr/bin/python
# Copyright 2015 - 2016 Boling Consulting Solutions, bcsw.net
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import unittest
import sys
import string
import random
import urllib
from ..restconfListInstance import RestconfListInstance


class RestconfListInstanceTest(unittest.TestCase):
    """
    Process the list-instance portion of an api-identifier where:

        list-instance = api-identifier "=" key-value ["," key-value]*

           key-value = string

           string = <a quoted or unquoted string>

         identifier = (ALPHA / "_") *(ALPHA / DIGIT / "_" / "-" / ".")
    """

    def test_string_identifier(self):
        uri = '=b'
        inst = RestconfListInstance(uri)
        self.assertFalse(inst.is_valid)
        self.assertNotEqual(len(inst.error_message), 0)

        uri = 'a='
        inst = RestconfListInstance(uri)
        self.assertFalse(inst.is_valid)
        self.assertNotEqual(len(inst.error_message), 0)

        uri = 'a="b"'
        inst = RestconfListInstance(uri)
        self.assertTrue(inst.is_valid)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), '"b"')
        self.assertEqual(type(inst.keys[0]), type('"b"'))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=b,c,d,e'
        inst = RestconfListInstance(uri)
        self.assertTrue(inst.is_valid)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 4)
        self.assertEqual(str(inst.keys[0]), 'b')
        self.assertEqual(str(inst.keys[1]), 'c')
        self.assertEqual(str(inst.keys[2]), 'd')
        self.assertEqual(str(inst.keys[3]), 'e')
        self.assertEqual(type(inst.keys[1]), type('c'))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=b,,"d"'
        inst = RestconfListInstance(uri)
        self.assertTrue(inst.is_valid)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 3)
        self.assertEqual(str(inst.keys[0]), 'b')
        self.assertEqual(str(inst.keys[1]), '')
        self.assertEqual(str(inst.keys[2]), '"d"')
        self.assertEqual(type(inst.keys[2]), type('"d"'))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=b,"",d'
        inst = RestconfListInstance(uri)
        self.assertTrue(inst.is_valid)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 3)
        self.assertEqual(str(inst.keys[0]), 'b')
        self.assertEqual(str(inst.keys[1]), '""')
        self.assertEqual(str(inst.keys[2]), 'd')
        self.assertEqual(type(inst.keys[0]), type('""'))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

    def test_int_identifier(self):
        uri = 'a=123'
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), 123)
        self.assertEqual(type(inst.keys[0]), type(123))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=-123'
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), -123)
        self.assertEqual(type(inst.keys[0]), type(-123))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=0'
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), 0)
        self.assertEqual(type(inst.keys[0]), type(0))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=-0'
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), -0)
        self.assertEqual(type(inst.keys[0]), type(-0))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

    def test_long_identifier(self):
        big_val = sys.maxint + sys.maxint
        uri = 'a=%d' % big_val
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), big_val)
        self.assertEqual(type(inst.keys[0]), type(big_val))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=%d' % -big_val
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), -big_val)
        self.assertEqual(type(inst.keys[0]), type(-big_val))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

    def test_float_identifier(self):
        uri = 'a=123.456789'
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), 123.456789)
        self.assertEqual(type(inst.keys[0]), type(123.456789))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=-123.456'
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), -123.456)
        self.assertEqual(type(inst.keys[0]), type(-123.456))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=0.456'
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), 0.456)
        self.assertEqual(type(inst.keys[0]), type(0.456))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=.456'
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), 0.456)
        self.assertEqual(type(inst.keys[0]), type(0.456))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=-0.456'
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), -0.456)
        self.assertEqual(type(inst.keys[0]), type(-0.456))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

    def test_boolean_identifier(self):
        uri = 'a=True'
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), True)
        self.assertEqual(type(inst.keys[0]), type(True))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=true'
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), 'a=True')
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), True)
        self.assertEqual(type(inst.keys[0]), type(True))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=False'
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), uri)
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), False)
        self.assertEqual(type(inst.keys[0]), type(False))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=false'
        inst = RestconfListInstance(uri)
        self.assertEqual(str(inst), 'a=False')
        self.assertEqual(len(inst.keys), 1)
        self.assertEqual(str(inst.keys[0]), False)
        self.assertEqual(type(inst.keys[0]), type(False))
        self.assertEqual(inst.module_name, None)
        self.assertEqual(len(inst.error_message), 0)

        uri = 'a=TRUE'
        inst = RestconfListInstance(uri)
        self.assertFalse(inst.is_valid)
        self.assertNotEqual(len(inst.error_message), 0)

        uri = 'a=FALSE'
        inst = RestconfListInstance(uri)
        self.assertFalse(inst.is_valid)
        self.assertNotEqual(len(inst.error_message), 0)

    def test_mixed_identifier(self):
        uri = 'a="b"'
        self.assertEqual("TODO", "Implement This")

    def test_module_name(self):
        uri = 'a="b"'
        self.assertEqual("TODO", "Implement This")
