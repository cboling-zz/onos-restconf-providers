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

    def test_identifier(self):
        uri = 'a="b"'
        self.assert_true(RestconfListInstance(uri).is_valid)

        # TODO: Lots more to do, include some failure checks
