# Developed by @BenjaminOBrien and kind of @Crcoli7307.

from render import clear

def loadpkg(path):

  data = open(path, "r").read()

  lines = data.split("\n")

  # loop through all the lines
  for line in lines:

    # ignore comments
    if line.startswith("--"):

      pass

    # system elements
    elif line.startswith("system."):

      element = line.replace("system.", "")

      if element.startswith("Write"):

        text = element[7:][:-2]

        print(text)

      elif element.startswith("Clear"):

        clear()