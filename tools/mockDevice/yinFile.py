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
import xml.etree.ElementTree
from xml.etree.ElementTree import QName
import pprint


class YINFile:
    """
    Class to support reading and parsing YIN file
    """
    namespace = None

    def __init__(self, file_path):
        """
        Initializer

        :param file_path: (string) Path to YIN file
        """
        self.path = file_path
        self.root = xml.etree.ElementTree.parse(file_path).getroot()

        if self.root.tag[0] == "{":
            self.namespace, _ignore1, _ignore2 = self.root.tag[1:].partition("}")
            container_tag = str(QName(self.namespace, 'container'))
        else:
            container_tag = 'container'

        self.containers = self.root.findall(container_tag)
        pass

    @property
    def file_path(self):
        """
        The file path related to this object

        :return: (string) YIN file path
        """
        return self.path

    @property
    def module_name(self):
        """
        :return: (string) The module name for this model.  None returned if not found
        """
        try:
            return self.root.attrib['name']
        except KeyError:
            return None

    @property
    def namespace(self):
        """
        :return: (string) The XML namespace for the file
        """
        return self.namespace

    @property
    def containers(self):
        """
        :return: (Element list) List of all top level containers
        """
        return self.containers

    def is_config(self, element, include_children=False):
        """
        Is an element, and optionally any children, are config-true

        :return: (boolean) True if the element has config-data 'true' properties
        """
        pass

    def _get_extmethods(element, path_base=''):
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
                extmethods.update(_get_extmethods(value, path_base=path))

        return extmethods

    def _fix_extmethods(extmethods):
        """
        Walk through the methods and fix up any parents that have no children that
        are writeable.
        """
        # TODO: Need to implement
        return extmethods
