import settings
import sys
sys.path.append('./utils/classes')

def update_dict(dict, key, value):
  
  for s in settings.servers:
    if s == dict:
      s[key] = value

  settings.rw.write(settings.servers)