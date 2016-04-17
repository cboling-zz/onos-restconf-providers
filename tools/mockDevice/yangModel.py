#
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
from yinFile import YINFile
from pyangbind.lib.base import PybindBase
from pyangbind.lib.yangtypes import YANGDynClass
from pyangbind.lib.yangtypes import YANGListType, TypedListType

import os
import pprint


class YangModel:
    """
    TODO: Document this
    """
    _extmethods = None
    _yang_class = None

    def __init__(self, yin_path, yin_file, model_dir, verbose=False):
        """
        TODO: Document this
        """
        self.yin = YINFile(os.path.join(yin_path, yin_file))
        self.model_dir = model_dir
        self.verbose = verbose  # gen_dir, filename, generated_dir,

        # Import the model
        self._import_models()
        pass

    @property
    def name(self):
        """
        TODO: Document this
        """
        return self.yin.module_name

    @property
    def extmethods(self):
        """
        TODO: Document this
        """
        if self._extmethods is None:
            self._extmethods = self._get_extmethods(self._yang_class().get())

        return self._extmethods

    def _import_models(self):
        """
        TODO: Document this
        """
        package = self.model_dir
        module = self.yin.module_name
        _class = self.yin.module_name

        try:
            if self.verbose > 0:
                print 'Dynamic import -> from %s.%s import %s' % (package, module, _class)

            yang_module = __import__('%s.%s' % (package, module), fromlist=[_class])
            self._yang_class = getattr(yang_module, _class)

            if self.verbose > 0:
                print 'YANG class imported: %s' % self._yang_class

                # TODO: This yang class is basic, we need to append the extmethods to it so we can support
                # everything we want to do

        except ImportError:
            print 'Import Error while attempting to import class %s from %s.%s' % (_class, package, module)

            # Instantiate the models the first time so we can generate all the paths within
            # them so we can create extension methods that provide for RESTCONF required
            # methods
            ###########################################################################

    def _get_extmethods(self, element, path_base=''):
        """
        A recursive function to convert a yang model into a extmethods dictionary

        :param element: (list of YANGDynClass) Child elements of a the model instance
        :param path_base: (dict) Existing dictionary of elements

        :return: (dict) A Pyangbind compatible extmethods dictionary
        """
        extmethods = {}

        if element is None:
            return extmethods

        if isinstance(element, dict):
            # print '%s is a dictionary of length %d' % (element, len(element))

            # yang_name = getattr(element, "yang_name") if hasattr(element, "yang_name") else None
            # is_container = hasattr(element, "get")

            for key, value in element.items():
                path = path_base + '/' + key
                config = True

                yang_name = getattr(value, "yang_name") if hasattr(element, "yang_name") else None
                is_container = hasattr(value, "get")

                try:
                    if value._is_leaf:  # Protected, but I really need to know
                        config = value.flags.writeable

                except AttributeError:
                    pass  # Was another dictionary item or did not have a writeable flag

                # Add this to our path
                extmethods[path] = config
                extmethods.update(self._get_extmethods(value, path_base=path))

        return extmethods

    def _fix_extmethods(self, extmethods):
        """
        Walk through the methods and fix up any parents that have no children that
        are writeable.
        """
        # TODO: Need to implement
        return extmethods
