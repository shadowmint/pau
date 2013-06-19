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

import unittest
import bootstrap
import pau
import os
from pau.model import *
from nark import *


class PrefTests(unittest.TestCase):

  # db for this test
  db_name = "PrefTests.sqlite"

  def setup(self):
    """ Setup db and return instance """

    # Setup test db
    print("%r" % pau.scope)
    self.config = pau.scope.resolve(pau.IConfig)
    self.session = pau.scope.resolve(pau.ISession)
    self.session.assets = Assets()
    self.config.db = self.db_name
    self.db = pau.scope.resolve(pau.IDb)
    self.db.init(self.config, self.session)

    # Instance
    i = Prefs()
    pau.resolve(i)
    return i

  def teardown(self):
    self.db.reset()
    try:
      os.remove(self.db_name)
    except:
      pass

  def test_can_create_instance(self):
    a = Assert()
    i = self.setup()
    a.not_null(i, "Unable to create instance")
    self.teardown()

  def test_can_insert(self):
    a = Assert()
    i = self.setup()
    i.add("Key", "Value")
    self.teardown()

  def test_can_get_by_name(self):
    a = Assert()
    i = self.setup()
    i.add("Key", "Value")
    record = i.get("Key")
    a.equals(record.value, "Value", "Failed to query db")
    self.teardown()

  def test_can_delete_record(self):
    a = Assert()
    i = self.setup()

    i.add("Key", "Value")
    found = i.has("Key")
    a.true(found, "Failed to found record")

    i.delete("Key")
    found = i.has("Key")
    a.false(found, "Found missing record")

    self.teardown()

  def test_can_update_record(self):
    a = Assert()
    i = self.setup()

    i.add("Key1", "Value")
    i.add("Key1", "Value2")
    i.add("Key1", "Value3")

    p = i.get("Key1")
    a.equals(p.value, "Value3", "Update didn't work")

    i.delete("Key1")
    found = i.has("Key1")
    a.false(found, "Multiple insert did not do an update")

    self.teardown()


if __name__ == "__main__":
  unittest.main()
