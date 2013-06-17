from nark import *
import json
import logging
import os
from os.path import join, abspath

def load_units(assets):
  """ Load all the units we can and return them as parsed dicts """
  rtn = {}
  invalid = {}
  try:
    path = assets.resolve("pa", "units", "unit_list.json")
    fp = open(path, 'r')
  except Exception:
    logging.error("Unable to locate units list. Bad PA install directory")
    return [], []
  units = json.load(fp)
  fp.close()
  list = units["units"]
  for l in list:
    try:
      udata = load_json(l, assets)
      while True:
        udata, done = load_base_unit(udata, assets)
        if done: 
          break
      rtn[l] = udata
    except Exception:
      e = exception()
      invalid[l] = e
  for k in rtn:
    print(k)
  for k in invalid:
    print("invalid: %s" % k)
  return rtn, invalid

def load_base_unit(udata, assets):
  """ Load the base_spec for a unit and combine 
      If no base_spec key, do nothing and return True
  """
  if "base_spec" in udata.keys():
    base_udata = load_json(udata["base_spec"], assets)
    udata.pop("base_spec", None)
    for k in udata.keys():
      base_udata[k] = udata[k]
    udata = base_udata
    return udata, False
  else:
    return udata, True

def load_json(path, assets):
  """ Load a single json file """
  udata = {}
  parts = path.split("/")
  full_path = assets.resolve(*parts)
  try:
    fp = open(full_path, 'r')
    udata = json.load(fp)
    fp.close()
  except Exception:
    e = exception()
    raise Exception("Bad json file '%s': %s" % (full_path, e))
  return udata
