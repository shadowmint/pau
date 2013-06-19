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


@resolve(pau.scope)
class Utils(object):
  
  def __init__(self, session=pau.ISession):
    self.session = session
    self.prefs = pau.model.Prefs()
    self.flash = pau.model.Flash()

  def reformat(self, key, value):
    """ Save the install path preference """
    try:
      location = self.prefs.get(pau.Preferences.LOCATION).value
      tmp = Assets(location)
      path = tmp.resolve(".")
    except Exception:
      self.flash.fail("Invalid path; you haven't set your PA install directory correctly")
      return {}

    # Try this job
    self.flash.notice("Processing files...")
    job = JsonReformatJob()
    job.start({"path" : path})
    return {}


class JsonReformatJob(nark.process.Worker):
  """ Run the json reformat job and log it """

  def context(self):
    self.flash = pau.model.Flash()

  def done(self):
    self.flash.success("Success! All files have been updated.")

  def local(self, data):
    self.api.listen(nark.process.WorkerEvents.TERMINATE, self.done)
    self.api.event_loop(wait=False)

  def remote(self, data):
    from pau.utils.json_reformat import reformat
    try:
      import time
      reformat(data["path"])
    except Exception:
      e = exception()
      self.flash.fail("Something went wrong: %s" % e)


# Logging
log = LogManager.get_logger()
