from __future__ import absolute_import
import bootstrap
from nark import *
import pau.less
import time
import datetime

less = pau.less.Less()
assets = Assets()
path = assets.resolve("..", "static", "css")
while True:
  less.execute(path)
  time.sleep(0.5)
  print("Updated: %s" % datetime.datetime.now())
