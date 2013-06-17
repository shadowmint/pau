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
import os
from nark import LogManager, run
from os.path import join


class Less(object):
  """ Less css compiler 

      lessc isn't installed?
      install instructions: http://lesscss.org/
  """

  def execute(self, path):
    """ Convert all .less files in the given path to .css """

    # Check and warn
    if not run("lessc", check_only=True):
      log.warn("lessc is not installed. Less files were not updated")
      return

    # Run
    for f in os.listdir(path):
      f = f.lower()
      if f[-5:] == ".less":
        fullpath = join(path, f)
        output_path = fullpath[:-5] + ".css"
        run("lessc", fullpath, output_path)


log = LogManager.get_logger();
