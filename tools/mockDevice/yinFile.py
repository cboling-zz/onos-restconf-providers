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
from pyangbind.lib.base import PybindBase
from pyangbind.lib.yangtypes import YANGDynClass
from pyangbind.lib.yangtypes import YANGListType, TypedListType
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

    def get_name_wo_namespace(self, fullname):
        """
        Extracts the simple name of an item without the namespace

        :param fullname: (string) Namespace + an element name

        :return: (string) Name without the namespace

        """
        return fullname.replace(self.namespace, '')

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

    def get_extmethods(self, root, element, path_base=''):
        """
        A recursive function to convert a yang model into a extmethods dictionary

        :param element: (dict) Child elements (YANGBaseClass or more dict) of a the model instance
        :param path_base: (dict) Existing dictionary of elements

        :return: (dict) A Pyangbind compatible extmethods dictionary
        """
        extmethods = {}

        if element is None:
            return extmethods

        if isinstance(element, dict):

            for key, value in element.items():
                path = path_base + '/' + key
                config = True

                # root.findall('./*[@name]')   Returns all children with a 'name' attribute
                # root.findall('./*[@name]')[0]  First matching child
                # root.findall('./*[@name]')[0].tag    -> first child tag such as string '{urn:ietf:params:xml:ns:yang:yin:1}identity'
                # root.findall('./*[@name]')[0].attrib -> first child attribute value such as dict {'name': 'genre'}

                # keywords = ['{urn:ietf:params:xml:ns:yang:yin:1}container','{urn:ietf:params:xml:ns:yang:yin:1}list','{urn:ietf:params:xml:ns:yang:yin:1}leaf']
                # xyz = [ x for x in root.findall('./*[@name]') if x.tag in keywords ]
                # xyz is a list of all children who have a name attribute and the tag is the namespace+keyword value

                # key = 'jukebox'
                # abc = [ x for x in root.findall('./*[@name]') if x.tag in keywords and x.attrib['name'] == key ]
                # print abc
                # [<Element '{urn:ietf:params:xml:ns:yang:yin:1}container' at 0x7f3b41cb0810>]

                # self.get_name_wo_namespace()

                # NOTES:
                # For containers, a 'presence'  is explicitly for config

                yang_name = getattr(value, "yang_name") if hasattr(element, "yang_name") else None
                is_container = hasattr(value, "get")

                try:
                    if value._is_leaf:  # Protected, but I really need to know
                        config = value.flags.writeable

                except AttributeError:
                    pass  # Was another dictionary item or did not have a writeable flag

                # Add this to our path
                extmethods[path] = config
                extmethods.update(self.get_extmethods(value, path_base=path))

        return extmethods

