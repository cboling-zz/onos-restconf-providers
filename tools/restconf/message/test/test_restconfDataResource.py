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
from ..restconfDataResource import RestconfDataResource


class RestconfDataResourceTest(unittest.TestCase):
    """
    api-path = "/" |
              ("/" api-identifier
              0*("/" (api-identifier | list-instance )))

              api-identifier = [module-name ":"] identifier                 ;; note 1

              module-name = identifier

              list-instance = api-identifier "=" key-value ["," key-value]*

              key-value = string                                            ;; note 1

              string = <a quoted or unquoted string>

      An identifier MUST NOT start with ((X|x) (M|m) (L|l))

             identifier = (ALPHA / "_") *(ALPHA / DIGIT / "_" / "-" / ".")

      Note 1: The syntax for "api-identifier" and "key-value" MUST conform to the
              JSON identifier encoding rules in Section 4 of [I-D.ietf-netmod-yang-json]
    """

    # _badStart = 'XxMmLl'      # TODO The MUST NOT start clause seems incorrect?
    _badStart = ''
    _goodStart = (string.ascii_letters + '_').translate(None, ''.join(_badStart))
    _validChars = string.ascii_letters + string.digits + '_-.'
    _invalidChars = string.printable.translate(None, ''.join(_validChars))
    _percentEncoded = urllib.quote(',:" /') + urllib.quote("'")

    def test_valid_identifier(self):
        """
        #   An identifier MUST NOT start with ((X|x) (M|m) (L|l))
        #
        #           identifier = (ALPHA / "_") *(ALPHA / DIGIT / "_" / "-" / ".")
        """
        for good in self._goodStart:
            self.assertTrue(good)

        for good in self._goodStart:
            self.assertTrue(good + self._validChars[random.randrange(0, len(self._validChars))])

        for bad in self._badStart:
            self.assertFalse(bad)

            for idx in range(0, len(self._validChars)):
                self.assertFalse(bad + self._validChars[idx])

        for bad in self._invalidChars:
            self.assertFalse(bad)
            self.assertFalse(self._goodStart[random.randrange(0, len(self._goodStart))] +
                             bad +
                             self._validChars[random.randrange(0, len(self._validChars))])

    def test_api_identifier_no_lists(self):
        """
        api-path = "/" |
                  ("/" api-identifier
                  0*("/" (api-identifier | list-instance )))

                  api-identifier = [module-name ":"] identifier                 ;; note 1

                  module-name = identifier

                  list-instance = api-identifier "=" key-value ["," key-value]*

                  key-value = string                                            ;; note 1

                  string = <a quoted or unquoted string>

        Note 1: The syntax for "api-identifier" and "key-value" MUST conform to the
                JSON identifier encoding rules in Section 4 of [I-D.ietf-netmod-yang-json]
        """
        resource = RestconfDataResource('/')
        self.assertTrue(resource.is_valid)
        self.assertEqual(len(resource.error_message), 0)
        self.assertEqual(len(resource.dict), 0)

        resource = RestconfDataResource('/abcd')
        self.assertTrue(resource.is_valid)
        self.assertEqual(len(resource.error_message), 0)
        self.assertEqual(len(resource.dict), 1)
        self.assertTrue('' in resource.dict)
        self.assertEqual(len(resource.dict['']), 1)
        self.assertEqual(resource.dict[''][0], 'abcd')

        resource = RestconfDataResource('/abcd/efgh')
        self.assertTrue(resource.is_valid)
        self.assertEqual(len(resource.error_message), 0)
        self.assertEqual(len(resource.dict), 1)
        self.assertTrue('' in resource.dict)
        self.assertEqual(len(resource.dict['']), 2)
        self.assertEqual(resource.dict[''][0], 'abcd')
        self.assertEqual(resource.dict[''][1], 'efgh')

        resource = RestconfDataResource('/abcd/efgh/ijkl')
        self.assertTrue(resource.is_valid)
        self.assertEqual(len(resource.error_message), 0)
        self.assertEqual(len(resource.dict), 1)
        self.assertTrue('' in resource.dict)
        self.assertEqual(len(resource.dict['']), 3)
        self.assertEqual(resource.dict[''][0], 'abcd')
        self.assertEqual(resource.dict[''][1], 'efgh')
        self.assertEqual(resource.dict[''][2], 'ijkl')

        resource = RestconfDataResource('/abcd:efgh')
        self.assertTrue(resource.is_valid)
        self.assertEqual(len(resource.error_message), 0)
        self.assertEqual(len(resource.dict), 1)
        self.assertTrue('abcd' in resource.dict)
        self.assertEqual(len(resource.dict['abcd']), 1)
        self.assertEqual(resource.dict['abcd'][0], 'efgh')

        resource = RestconfDataResource('/abcd:efgh/ijkl')
        self.assertTrue(resource.is_valid)
        self.assertEqual(len(resource.error_message), 0)
        self.assertEqual(len(resource.dict), 1)
        self.assertTrue('abcd' in resource.dict)
        self.assertEqual(len(resource.dict['abcd']), 2)
        self.assertEqual(resource.dict['abcd'][0], 'efgh')
        self.assertEqual(resource.dict['abcd'][1], 'ijkl')

        resource = RestconfDataResource('/abcd:efgh/ijkl:mnop/qrst')
        self.assertTrue(resource.is_valid)
        self.assertEqual(len(resource.error_message), 0)
        self.assertEqual(len(resource.dict), 2)
        self.assertTrue('abcd' in resource.dict)
        self.assertTrue('mnop' in resource.dict)
        self.assertEqual(len(resource.dict['abcd']), 2)
        self.assertEqual(resource.dict['abcd'][0], 'efgh')
        self.assertEqual(resource.dict['abcd'][1], 'ijkl')
        self.assertEqual(len(resource.dict['mnop']), 1)
        self.assertEqual(resource.dict['mnop'][0], 'qrst')

        resource = RestconfDataResource('/abcd/')
        self.assertFalse(resource.is_valid)
        self.assertGreater(len(resource.error_message), 0)
        self.assertEqual(len(resource.dict), 0)

        resource = RestconfDataResource('/:')
        self.assertFalse(resource.is_valid)
        self.assertGreater(len(resource.error_message), 0)
        self.assertEqual(len(resource.dict), 0)

        resource = RestconfDataResource('/abcd:')
        self.assertFalse(resource.is_valid)
        self.assertGreater(len(resource.error_message), 0)
        self.assertEqual(len(resource.dict), 0)

    def test_api_identifier_lists(self):
        """
        api-path = "/" |
                  ("/" api-identifier
                  0*("/" (api-identifier | list-instance )))

                  api-identifier = [module-name ":"] identifier                 ;; note 1

                  module-name = identifier

                  list-instance = api-identifier "=" key-value ["," key-value]*

                  key-value = string                                            ;; note 1

                  string = <a quoted or unquoted string>

        Note 1: The syntax for "api-identifier" and "key-value" MUST conform to the
                JSON identifier encoding rules in Section 4 of [I-D.ietf-netmod-yang-json]
        """
        pass

    def test_api_key_value(self):
        """
                  key-value = string                                            ;; note 1

                  string = <a quoted or unquoted string>

        Note 1: The syntax for "api-identifier" and "key-value" MUST conform to the
                JSON identifier encoding rules in Section 4 of [I-D.ietf-netmod-yang-json]
        """
        pass

    def test_key_value(self):
        """
        Note 1: The syntax for "api-identifier" and "key-value" MUST conform to the
                JSON identifier encoding rules in Section 4 of [I-D.ietf-netmod-yang-json]
        """
        resource = RestconfDataResource('module:api')

        self.assertTrue(resource.isValid)

        # TODO Test percent encoded values of   (,':" /)
