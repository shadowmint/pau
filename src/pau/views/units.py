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
import nark.process
import pau.model
import pau
from pau.utils.unit_query import load_units


@resolve(pau.scope)
class Units(object):
  
  def __init__(self, session=pau.ISession):
    self.session = session
    self.prefs = pau.model.Prefs()
    self.flash = pau.model.Flash()

  def load(self, key, value):
    """ Save the install path preference """
    data = {}
    try:
      location = self.prefs.get(pau.Preferences.LOCATION).value
      tmp = Assets(location)
      data, invalid = load_units(tmp)
    except Exception:
      e = exception()
      self.flash.fail("Failed: %s" % e)
      return {}
    for i in invalid:
      self.flash.notice("Warning, failed to load: %s: %s" % (i, invalid[i]))
    self.flash.success("Loaded unit data!")
    return data


# Logging
log = LogManager.get_logger()
