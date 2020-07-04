import logging
from os import getcwd

import CLI.func as CLI
from time import sleep

from flask import Flask
from render import clear

from colors import color
from threading import Thread

from os import listdir, chdir
from packages.load import loadpkg

from os.path import exists, isfile

def _run(port, text):

  app = Flask(__name__)

  log = logging.getLogger("werkzeug")

  log.disabled = True

  app.logger.disabled = True

  @app.route("/")
  def index():
    return text

  app.run(host = "0.0.0.0", port = port)

def parse(cmd, args, config, startSystem):

  if cmd.lower() in ["sys", "system", "sys-stats"]:

    CLI.system()

  elif cmd.lower() in ["cls", "clear"]:

    clear()

  elif cmd.lower() in ["help", "info"]:

    CLI.help(config)

  elif cmd.lower() in ["license"]:

    CLI.license()

  elif cmd.lower() in ["logout", "lgt"]:

    startSystem(doBoot = False)

  elif cmd.lower() in ["tree", "list"]:

    try:

      _ = args[0]

      path = ""

      for arg in args:

        path += arg + " "

      path = path[:-1]

    except:

      path = getcwd()

    try:

      chdir(path)

      paths = listdir()

      items = []
      
      dirs = []

      print()

      for _path in paths:

        if isfile(_path):

          items.append(_path)

        else:

          dirs.append(_path)

      for dir in dirs:

        items.append(dir)

      for _path in items:

        if isfile(_path):

          print(f"- {_path}")

        else:

          print("---|")

          print(f"   --- {_path}")

      print()

    except:

      print("\nSpecified path does not exist.\n")

  elif cmd.lower() in ["server", "sv"]:

    if not args:

      print("\nUsage: server [host] [port] [text]\n")

    else:

      try:

        host = args[0]

        port = args[1]

        text = ""

        for arg in args[2:]:

          text += arg + " "

        try:

          port = int(port)

          thread = Thread(target = _run, args = [port, text])

          thread.start()

          sleep(.5)

          clear()

          print(f"\nServer now running at {host}:{port}\n")

        except:

          print("\nInvalid port specified.\n")

      except:

        print("\nUsage: server [host] [port] [text]\n")

  elif cmd.lower() in ["pkg", "package"]:

    if not args:

      print("\nUsage: pkg [path]\n")

    else:

      try:

        path = ""

        for arg in args:

          path += arg + " "

        path = path[:-1]

        if not path:

          print("\nNo package path specified.\n")

        else:

          if not exists(path):

            print("\nSpecified path does not exist.\n")

          else:

            if not path.endswith(".zeal"):

              print("\nSpecified path does not contain a ZealousOS package.\n")

            else:

              print()

              loadpkg(path)

              print()

      except:

        print("\nNo package path specified.\n")

  elif cmd.lower() in ["echo", "write", "print"]:

    if not args:

      pass

    else:

      text = ""

      for arg in args:

        text += arg + " "

      print(f"\n{text[:-1]}\n")

  elif cmd.lower() in ["reboot", "rbt"]:

    print(f"Rebooting system...{color('reset')}")

    startSystem()

  elif cmd.lower() == "":

    pass

  else:

    print(f"\nCommand \"{cmd}\" not found.\n")