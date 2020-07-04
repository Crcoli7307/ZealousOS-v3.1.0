from os import listdir
from time import sleep

from render import clear
from colors import color

from os.path import isfile
from system import Service

file_raws = {}

def main():

  for file in listdir():

    if isfile(file):

      file_raws[file] = open(file, "r").read()

  while True:

    sleep(60)

    for file in listdir():

      if isfile(file):

        raw_data = open(file, "r").read()

        try:
            
          if not raw_data == file_raws[file]:

            while True:

              clear()

              print(color("red"))

              print("[ANTVIRUS]: File change detected while the OS was in use.")

              print("[ANTVIRUS]: Please restore the file and reboot.")

              sleep(.4)
        except:

          pass

antivirus = Service(
  name = "Antivirus",
  func = main
)