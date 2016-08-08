#
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
from flask import Blueprint, abort, url_for
from jinja2 import TemplateNotFound
import os.path
from datetime import datetime

# from testDevice import app            # TODO: Clean this up later
# __basePath = os.path.join('/', root_resource, 'data')

# Look into http://flask.pocoo.org/docs/0.10/views/
# also look at: http://flask.pocoo.org/docs/0.10/blueprints/
# http://stackoverflow.com/questions/13317536/get-a-list-of-all-routes-defined-in-the-app

dataStore = Blueprint('dataStore', __name__)


@dataStore.route('/', defaults={'module': '-all-'})
@dataStore.route('/<module>')
def show(module):
    """
    :param module: (string) submodule
    """
    try:
        # return render_template('pages/%s.html' % module)
        if module is None:
            module = 'None'
        return 'hello world: %s' % module
    except TemplateNotFound:
        abort(404)


class DataStore:
    """
    Base class for objects in the RESTCONF Datastore Resource tree {+restconf}/data
    """
    methods = ['GET']
    fullPath = ''
    theApp = None
    lastModifiedTimestamp = datetime.utcnow()

    def __init__(self, path):
        """
        Initializer for base DataStore class

        :param path: (string) the resource path based of the '{+restconf}/data/' subtree
        """
        # View.__init__(self)
        # self.theApp = app
        self.path = os.path.join(self.basePath, path)

    @property
    def uri(self):
        """
        :return: (string) the full datastore URI (URL less http[s]://<ip-address[:port]> prefix)
        """
        return self.path

    @property
    def last_modified(self):
        """
        :return: (datetime) the UTC timestamp that this tree was last modified
        """
        return self.lastModified

    @last_modified.setter
    def last_modified(self, value):
        """
        Set the last modified time.  Derived class should call their base class with
        the same 'value' so that it peculates up the tree.
        :param value: (datetime) new last modified timestamp (UTC)
        """
        self.lastModifiedTimestamp = value

    def get(self):
        # walk all the modules and return them

        urls = []
        for rule in app.url_map.iter_rules():
            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)
            url = url_for(rule.endpoint, **options)
            urls.append(url)

            # TODO: Do something with the urls
