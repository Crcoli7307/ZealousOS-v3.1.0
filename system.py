from time import sleep
from requests import get

from datetime import date
from os.path import exists

from getpass import getpass
from threading import Thread

from psutil import getloadavg
from json import dumps, loads

from colors import colored, color
from render import clear, multiLine, singleLine

def setup():

  while True:

    clear()

    print("Welcome to the ZealousOS setup utility.")

    print("To get started, you need to make a ZealousOS account.")

    print()

    try:

      username = input("Account Username: ")

      password = getpass("Account Password: ")

      confirm_password = getpass("Confirm Password: ")

    except KeyboardInterrupt:

      return

    if not password == confirm_password:

      print()

      print(colored("Passwords do not match! Retrying in 3 seconds..", "red"))

      sleep(3)

    else:

      break

  user = {
    "username": username,
    "password": password
  }

  open("data/user.json", "w").write(dumps(user, indent = 4))

def fetchUser():

  user = loads(open("data/user.json", "r").read())

  if not "username" in user:

    return {
      "username": "root",
      "password": "root"
    }

  return user

def checkFiles():

  status = True

  file_list = [
    "main.py", "render.py", "system.py",
    "data/user.json", "icons/bootLogo.txt",
    "data/os.json", "colors.py", "CLI/func.py", "CLI/parser.py",
    "antivirus/service.py"
  ]

  for file in file_list:

    if not exists(file):

      status = False

  return status

def checkPerformance():

  if getloadavg()[0] > 5:

    return False, getloadavg()[0]

  return True, getloadavg()[0]

def initialize(REQ_FIRST_TIME_SETUP):

  try:

    def init(text, time, action, args = None):

      multiLine(text)

      status = None

      if args:

        status = action(args)

      else:

        status = action()

      sleep(time)

      if not status:

        singleLine(colored("  [FAILED]", "red"))

      else:

        singleLine(colored("  [PASSED]", "green"))

      sleep(.7)

    multiLine("Checking user information..")

    sleep(.75)

    userData = loads(open("data/user.json", "r").read())

    if not "username" in userData:

      REQ_FIRST_TIME_SETUP = True

      singleLine(colored("  [NOT SETUP]", "yellow"))

    else:

      singleLine(colored("  [PASSED]", "green"))

    sleep(.7)

    init("Checking file states..", .75, checkFiles)

    multiLine("Checking system performance..")

    status, avg = checkPerformance()

    sleep(.75)

    if not status:

      singleLine(colored(f"  [FAILED] ({avg})", "red"))

    else:

      singleLine(colored("  [PASSED]", "green"))

    init("Checking CLI status..", 3.5, exists, "CLI")

    init("Checking modules..", 2, date.today)

    multiLine("Checking network status..")

    status = get("https://www.google.com").status_code

    sleep(3.5)

    if not status == 200:

      singleLine(colored("  [FAILED]", "red"))

    else:

      singleLine(colored("  [PASSED]", "green"))

    sleep(.7)

    print(colored("\nBooting..", "yellow"))

    sleep(2.7)

    return REQ_FIRST_TIME_SETUP

  except:

    raise KeyboardInterrupt("Boot manually canceled by host.")

def login(config):

  while True:

    clear()

    payload = fetchUser()

    print(colored(f"ZealousOS v{config['version']} | Login | {date.today()}", "blue"))

    try:

      username = input(colored("Username: ", "blue") + color("green"))

      password = getpass(colored("Password: ", "blue"))

    except:

      login(config)

    if not username or not password:

      login(config)

    elif not username == payload["username"] or not password == payload["password"]:

      print()

      print(colored("Invalid username or password! Retrying in 3 seconds..", "red"))

      sleep(3)

    else:
      
      break

  print()

  print(colored(f"Welcome to ZealousOS, {payload['username']}.", "green"))

  return username, password

class Service():

  def __init__(self, name, func):
    self.name = name
    self.task = func

  def start(self):
    t = Thread(target = self.task)
    t.start()