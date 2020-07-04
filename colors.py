colors = {
  "RED": "\x1b[31m \x1b[0m",
  "GREEN": "\x1b[32m \x1b[0m",
  "YELLOW": "\x1b[33m \x1b[0m",
  "BLUE": "\x1b[36m \x1b[0m",
  "RESET": "\033[0;0m"
}

def colored(text, color):

  return colors[color.upper()].replace(" ", text)

def color(color):

  return colors[color.upper()].split(" ")[0]