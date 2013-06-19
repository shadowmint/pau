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
from .config import IConfig
from .session import ISession
from .model.base import Base
from nark import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class IDb():

  def init(self):
    """ Init the db """
    pass

  def reset(self):
    """ Reset the db so a new init returns a new session """
    pass


@implements(IDb)
class Db():

  def __init__(self):
    self.config = None
    self.app = None
    self.engine = None

  def init(self, config, session):
    """ Create the local database if required """
    self.config = config
    self.session = session
    if self.engine is None:
      assets = self.app.assets
      path = assets.new(self.config.db)
      spath = "sqlite:///%s" % path
      engine = create_engine(spath, echo=self.config.db_debug)
      session = sessionmaker(bind=engine)
      self.__session = session
      self.engine = engine
      self.session = self.__session() # Instance
      if not self.app.assets.exists(path):
        try: 
          Base.metadata.create_all(self.engine)
          self.reset()
          self.init()
        except Exception:
          e = exception()
          raise Exception("Invalid db: '%s': %s" % (spath, str(e)))

  def reset(self):
    """ Rebuild all the things """
    if self.engine is not None:
      self.session.close()
      self.engine = None
