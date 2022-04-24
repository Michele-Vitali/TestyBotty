import json
import sys
sys.path.append('./guild.py')
import guild as g

import os

class ReaderWriter:
  def __init__(self, filePath):
    self.file = filePath

  def read(self):
    #Inizializzo una list vuota
    servers = []
    try:
      #Provo ad aprire il file in modalità di lettura
      with open(self.file, "r") as f:
        try:
          #Provo a leggere il file che viene trasformato in un array di oggetti json
          servers = json.load(f)
        except:
          print("The file you were trying to read does not contain any server")
    except:
      print("Couldn't read the given file")
    #Ritorno la lista
    return servers

  def write(self, servers):
    #Controllo se la lista è vuota
    if servers:
      try:
        #Provo ad aprire il file in modalità append
        with open(self.file, "a") as f:
          json.dump(servers, f, ensure_ascii = True, indent = 4)
      except:
        print("Couldn't open the file")
    else:
      try:
        #Se è vuota apro e chiudo il file così da cancellarne il contenuto interamente
        f = open(self.file, "w").close()
      except:
        print("Couldn't open the file")