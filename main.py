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
import models
import urllib
import hashlib
import datetime
import sessions
import time
import flash
import amazon
import logging
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from django.utils import simplejson
from google.appengine.api import memcache
from google.appengine.runtime import DeadlineExceededError
from passwd_crypto import hash_password
from dj import check_login

def getPath(filename):
  return os.path.join(os.path.dirname(__file__), filename)

class MainPage(webapp.RequestHandler):
  def get(self):
    self.sess = sessions.Session()
    self.flash = flash.Flash()
    album_list = []
    # album_list = models.getNewAlbums(50)
    start = datetime.datetime.now() - datetime.timedelta(weeks=1)
    end = datetime.datetime.now()
    song_num = 10
    album_num = 10
    top_songs, top_albums = models.getTopSongsAndAlbums(
      start, end, song_num, album_num)
    posts = models.getLastPosts(3)
    events = models.getEventsAfter(datetime.datetime.now() - 
                                   datetime.timedelta(days=1), 3)
    template_values = {
      'flash': self.flash,
      'session': self.sess,
      'album_list': album_list,
      'top_songs': top_songs,
      'top_albums': top_albums,
      'posts': posts,
      'events': events,
      }
    self.response.out.write(template.render(getPath("index.html"), 
                                            template_values))

def real_main():
  application = webapp.WSGIApplication([
      ('/', MainPage),
      ],
                                       debug=True)
  util.run_wsgi_app(application)

main = real_main
if __name__ == '__main__':
  main()
