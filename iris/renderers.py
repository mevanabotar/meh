
import blessed
terminal = blessed.Terminal()


def render_fore_color(hexrep):
 red, green, blue = hexrep[:2], hexrep[2:4], hexrep[4:6]
 r,g,b = [int(i, base=16) for i in [red, green, blue]]
 sgr = terminal.color_rgb(r, g, b)
 return sgr 

def render_back_color(hexrep):
 red, green, blue = hexrep[:2], hexrep[2:4], hexrep[4:6]
 r,g,b = [int(i, base=16) for i in [red, green, blue]]
 sgr = terminal.on_color_rgb(r, g, b)
 return sgr 


def render_bold(val):
 vl = int(val)
 retn = '\033[{}m'.format(1 if vl else 22)
 return retn

def render_italic(val):
 vl = int(val)
 retn = '\033[{}m'.format(3 if vl else 23)
 return retn


def render_underline(val):
 vl = int(val)
 retn = '\033[{}m'.format(4 if vl else 24)
 return retn


def render_reverse(val):
 vl = int(val)
 retn = '\033[{}m'.format(7 if vl else 27)
 return retn
