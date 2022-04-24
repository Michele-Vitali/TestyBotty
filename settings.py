import sys
sys.path.append('./utils/classes')
import readerWriter as rewr

def init():
  global rw
  global servers
  rw = rewr.ReaderWriter("./utils/data/guilds.json")
  servers = rw.read()