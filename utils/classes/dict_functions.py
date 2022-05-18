import settings

def update_dict(dict, key, value):
  
  for s in settings.servers:
    if s == dict:
      s[key] = value