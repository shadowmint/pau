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


@resolve(pau.scope)
class Setup(object):
  
  def __init__(self, session=pau.ISession):
    self.session = session
    self.prefs = pau.model.Prefs()
    self.flash = pau.model.Flash()

  def save_install_path(self, key, value):
    """ Save the install path preference """
    if value[-4:] == ".app":  # Probably a mac application. Dammit
      value = value + "/Contents/Resources"
    self.prefs.add(pau.Preferences.LOCATION, value)
    tmp = Assets(value)
    if not tmp.exists("pa"):
      self.flash.fail("Directory selected, but the path '{PATH}/pa' was missing. Maybe wrong folder?")
    else:
      self.flash.success("Selected PA install directory successfully")
    log.info("Updated PA install path to: %s" % value)
    return {}

  def choose_install_path(self, key, value):
    """ Selects an install folder via popup """
    path = self.session.webkit.select_file()
    return {"path":path}


# Logging
log = LogManager.get_logger()
