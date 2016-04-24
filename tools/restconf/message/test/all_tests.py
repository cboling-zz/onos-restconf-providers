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
import os
import glob
import unittest


def create_test_suite():
    # Get the relative directory path to this subdirectory
    rel_path = os.path.dirname(os.path.relpath(__file__))

    test_files = glob.glob('%s/test_*.py' % rel_path)

    module_strings = [module.replace('/', '.')[:len(module) - 3] for module in test_files]

    suites = [unittest.defaultTestLoader.loadTestsFromName(name)
              for name in module_strings]

    return unittest.TestSuite(suites) if len(suites) > 0 else None
