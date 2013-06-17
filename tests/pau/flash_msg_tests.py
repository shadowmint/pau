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


class FlashMsgTests(unittest.TestCase):

  # db for this test
  db_name = "FlashMsgTests.sqlite"

  def setup(self):
    """ Setup db and return instance """

    # Setup test db
    self.config = pau.IConfig
    self.session = pau.ISession
    pau.resolve(self)
    self.session.assets = Assets()
    self.config.db = self.db_name
    self.config.db_debug = False

    # Load db for reset later
    self.db = pau.IDb
    pau.resolve(self)

    # Instance
    i = Flash()
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

  def test_can_add_fail(self):
    a = Assert()
    i = self.setup()

    i.fail("That was dumb")
    a.true(i.any(), "Didn't create a message")

    value = i.get()
    a.equals(value.level, FlashTypes.FAILURE, "Added flash message didn't have the right type")
    a.false(i.any(), "Didn't remove a message")

    self.teardown()

  def test_can_add_notice(self):
    a = Assert()
    i = self.setup()

    i.notice("That was a notice")
    a.true(i.any(), "Didn't create a message")

    value = i.get()
    a.equals(value.level, FlashTypes.NOTICE, "Added flash message didn't have the right type")
    a.false(i.any(), "Didn't remove a message")

    self.teardown()

  def test_can_add_success(self):
    a = Assert()
    i = self.setup()

    i.success("That was successful!")
    a.true(i.any(), "Didn't create a message")

    value = i.get()
    a.equals(value.level, FlashTypes.SUCCESS, "Added flash message didn't have the right type")
    a.false(i.any(), "Didn't remove a message")

    self.teardown()


if __name__ == "__main__":
  unittest.main()
