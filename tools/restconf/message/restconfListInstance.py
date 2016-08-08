# Copyright 2015-present Boling Consulting Solutions, bcsw.net
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
import string
import sys
from restconfDataResource import RestconfDataResource


class RestconfListInstance(object):
    """
    Wraps RESTCONF list-instance URIs

    The module name, if any, should have already been stripped by and provided as input
    to the object constructor

        api-identifier = [module-name ":"] identifier

        list-instance = api-identifier "=" key-value ["," key-value]*

        key-value = string                                            ;; note 1

        string = <a quoted or unquoted string>
    """
    _error_message = ''
    _keys = []

    def __init__(self, identifier, module_name=None):
        self._identifier = ''
        self._module_name = module_name
        self._valid = self._parse_list_instance(module_name, identifier)

    def _parse_list_instance(self, module_name, list_instance):
        """
        Process the list-instance portion of an api-identifier where:

            list-instance = api-identifier "=" key-value ["," key-value]*

               key-value = string

               string = <a quoted or unquoted string>

        :param module_name: (string) The module-name
        :param list_instance: (string) The identifier

        :returns: (boolean) True if successfully parsed.
        """
        # This is either an identifier or a list-instance.  List-instances will always contain
        # and "=" since it is not a valid instance character

        instance_and_keys = list_instance.split('=')

        if len(instance_and_keys) != 2 or len(instance_and_keys[1].strip()) == 0:
            self._error_message = "Invalid list-instance '%s' found in resource path: '%s'" % \
                                  (list_instance, self._resource)
            return False

        self._identifier = instance_and_keys[0]

        if not RestconfDataResource.valid_identifier(self._identifier):
            self._error_message = "Invalid Identifier '%s' found in list-instance resource path: '%s'" % \
                                  (self._identifier, list_instance)
            return False

        # Encode the keys now

        return self._validate_keys(instance_and_keys[1].split(','))

    def _validate_and_modify_keys(self, key_list):
        """
        Validate the key syntax and optionally change it from a string to a more appropriate
        object type (int, boolean, ...)

        Keys can be an empty string, strings, ints, floats, ...
        """
        # TODO: How do we handle -0, do we keep a 'minus' flag available?

        for key in key_list:
            new_value = key
            if not any(x not in key for x in string.whitespace):
                try:
                    new_value = float(key)
                except (TypeError, ValueError):
                    try:
                        if key in ['True', 'true']:  # TODO: Do we really want this conversion (or leave as string?)
                            new_value = True
                        elif key in ['False', 'false']:
                            new_value = False
                        else:
                            raise TypeError
                    except (TypeError, ValueError):
                        try:
                            new_value = long(key)
                            if -sys.maxint - 1 <= key <= sys.maxint:
                                new_value = int(key)
                        except (TypeError, ValueError):
                            pass

            self._keys.extend([new_value])

        return True

    @property
    def is_valid(self):
        return self._valid

    @property
    def error_message(self):
        return self._error_message

    @property
    def module_name(self):
        return self._module_name

    @property
    def keys(self):
        return self._keys

    def __str__(self):
        str_val = '%s=' % self._identifier
        first = True
        for key in self._keys:
            if not first:
                str_val += ','
            str_val += '%s' % str(key)
            first = False

        return str_val
