# Copyright 2013 Douglas Linder
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from nark import *
import pau.model
import pau


class Home(object):
  
  def __init__(self):
    self.prefs = pau.model.Prefs()
    self.flash_service = pau.model.Flash()
    pau.resolve_children(self)

  def sample(self, key, value):
    return {"Result" : value["Hello"] + "World " + key}

  def has_setup(self, key, value):
    """ Check if the setup has been run at least once """
    rtn = {"result":True}
    if not self.prefs.has(pau.Preferences.LOCATION):
      rtn["result"] = False
    return rtn

  def preference(self, key, value):
    """ Check if the setup has been run at least once """
    rtn = {"result":""}
    if self.prefs.has(value):
      rtn["result"] = self.prefs.get(value).value
    return rtn

  def flash(self, key, value):
    """  Return the next flash message, if any """
    rtn = {"result" : False, "level" : False}
    if self.flash_service.any():
      msg = self.flash_service.get()
      rtn["result"] = msg.message
      if msg.level == pau.model.FlashTypes.FAILURE:
        rtn["level"] = "FAILURE"
      elif msg.level == pau.model.FlashTypes.SUCCESS:
        rtn["level"] = "SUCCESS"
      elif msg.level == pau.model.FlashTypes.NOTICE:
        rtn["level"] = "NOTICE"
    return rtn
