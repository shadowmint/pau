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
from .controller import Controller
from .config import *
from .db import *
from .session import *
from .consts import *


# Create common resolver
resolver = Resolver()
resolver.register(Config)
resolver.register(Db)
resolver.register(Session)
resolve = resolver.resolve
resolve_children = resolver.resolve_children

# Sometimes threads need their own specific context
def create_resolver():
  resolver = Resolver()
  resolver.register(Config)
  resolver.register(Db)
  resolver.register(Session)
  return resolver


__all__ = [
  'Controller',
  'IConfig',
  'IDb',
  'ISession',
  'resolve',
  'resolve_children',
  'create_resolver',
  'Preferences',
]
