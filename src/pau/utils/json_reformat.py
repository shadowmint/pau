import os
import json
from os.path import join
from nark import *

def reformat(path):
  for root, dirnames, filenames in os.walk(path):
    for f in filenames:
      f = f.lower()
      if f[-5:] == ".json":
        fullpath = join(root, f)
        log.info("Processed: %s" % fullpath)
        fp = open(fullpath)
        data = json.load(fp)
        fp.close()
        fp = open(fullpath, 'w')
        fp.write(json.dumps(data, indent=2, sort_keys=True))
        fp.close()


# Logging
log = LogManager.get_logger()
