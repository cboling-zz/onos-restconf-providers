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

import mockDevice.test.all_tests as mock_tests
import mockDevice.resource.test.all_tests as mock_resource_tests
import restconf.message.test.all_tests as restconf_msg_tests

all_suites = [mock_tests.create_test_suite(),
              mock_resource_tests.create_test_suite(),
              restconf_msg_tests.create_test_suite()]

for test_suite in all_suites:
    if test_suite is not None:
        text_runner = unittest.TextTestRunner().run(test_suite)
