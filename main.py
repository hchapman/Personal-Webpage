#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import urllib
import hashlib
import datetime
import time
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from django.utils import simplejson
from google.appengine.api import memcache
from google.appengine.runtime import DeadlineExceededError

SEMESTERS = {("fall", 0),
             ("spring", 1),
             ("summer", 2)}

def getPath(filename):
  return os.path.join(os.path.dirname(__file__), filename)

def parseClass(classname):
  pass

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render(getPath("index.html"), 
                                            dict()))

class ClassList(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render(getPath("class_list.html"), 
                                            dict()))

class ClassPage(webapp.RequestHandler):
  def get(self, semester, year, section):
    self.response.out.write(template.render(getPath("class_page.html"),
                                            dict()))


class ResearchPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render(getPath("index.html"), 
                                            dict()))

class OtherPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render(getPath("index.html"), 
                                            dict()))

def real_main():
  application = webapp.WSGIApplication([
      ('/', MainPage),
      ('/main/?', MainPage),
      ('/class/?', ClassList),
      ('/class/([^/]*)/([^/]*)/([^/]*)/?', ClassPage),
      ('/research/?', ResearchPage),
      ('/other/?', OtherPage),
      ],
                                       debug=True)
  util.run_wsgi_app(application)

main = real_main
if __name__ == '__main__':
  main()
