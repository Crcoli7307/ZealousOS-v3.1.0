import sys
from time import sleep
from os import system, name

def load(rotations = 10, text = "Loading..."):

  try:

    c = 0

    while c < rotations:

      print (f"-  {text}")

      sleep(0.1)

      clear()

      print (f"\\  {text}")

      sleep(0.1)

      clear()

      print (f"|  {text}")

      sleep(0.1)

      clear()

      print (f"/  {text}")

      sleep(0.1)

      clear()

      c += 1

  except:

    raise KeyboardInterrupt("Boot manually canceled by host.")
    
def clear():

  if name == "nt":

    system("cls")

  else:

    system("clear")

def multiLine(text):

  sys.stdout.write(text)

  sys.stdout.flush()

def singleLine(text):

  multiLine(text)

  print()