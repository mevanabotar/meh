
#Pg imports
from random import randint
import re
import functools

import blessed

from mytests.blessedtst import ekatn, rendr, prerendr, simplemap1, incompletemap1
from mytests.kairos import timer_resolution
from memoization import Memo
from iris import pupil
from iris import renderers


#Pg begin

terminal = blessed.Terminal()

#Pg helpers

def echo(toprint):
 """Print to terminal, always flushing and end in ''."""
 print(toprint, end='', flush=True)

def keywity(context_man):
 """Read a key pressed in the given context. Used for debugging."""
 with context_man():
  return terminal.inkey()

def rotate_to_half(index, whole):
 return index - whole //2

def down_to_closest_odd(num):
 offset = (num - 1) % 2
 return num - offset

#Pg cursor

class LoopRibbon():
 
 def __init__(self, source, renderer):
  self.string = source
  self.source = list(source)
  self.renderer = renderer
  self.rendered = Memo()

 def slice(self, start, delta):
  return [self.source[i % len(self)] for i in range(start, start+delta)]

 def find_from(self, pattern, start):
  patn = re.compile(pattern)
  matched = patn.search(self.string, start)
  return matched.start(), matched.end()

 def render(self, start, delta):

  if self.renderer is not None:
   """
   #Tag optimization: reduce the number of calls to render by memoizing already rendered values
   prerendered = self.rendered.get_slice(start, delta) 
   #I don't know how to integrate memoization with styleobj, so I'll leave it out for now.
   if prerendered is not None:
    return prerendered

   hererendered = self.renderer(self.slice(start, delta))
   self.rendered.add_slice(start, delta, hererendered)
   self.rendered.consolidate()
   return hererendered 
   """
   return self.renderer(self.slice(start, delta))

  return self.slice(start, delta)

 def duplicate(self):
  return self

 def __len__(self):
  return len(self.source)

 def __getitem__(self, index):
  return list.__getitem__(self.source, index)


class Head():

 def __init__(self, x, data):
  self.current = x
  self.update_position(x, len(data))
  self.track = data

 def update_position(self, new, loop):
  self.previous = self.current
  self.current = new % loop 
  self.x = self.current

 def mv_x(self, jump):
  self.update_position(jump, len(self.track))

 def mv_step(self, step):
  self.mv_x(self.x + step)

 def mv_left(self):
  self.mv_step(-1)

 def mv_right(self):
  self.mv_step(1)

 def find_from(self, pattern, start):
  s, e = self.track.find_from(pattern, start)
  return s, e

 def insert_cursor_at(self, lista, pos):
  lista[pos] = pupil.StyleObj(['','','','','1'], lista[pos])
  return lista

 def render(self, width, target_flag=False):
  texto = self.track.render(self.x, width)
  r, g, b = [randint(0,200) for i in [1, 2, 3]]
  print(f"\033[48;2;{r};{g};{b}m", texto , "\033[0m")
  #if target_flag:
   #texto = self.insert_cursor_at(datt, 0)
  #else:
   #texto = datt
  return pupil.StyleObj(['','','','',''], texto)

# multilines

class HeadArray():

 def __init__(self, headnum, datass, relren):

  self.datass = datass
  self.relren = relren
  self.headarr = [Head(0, self.datass.duplicate()) for i in range(headnum)]
  self.target_head = 0

 def rotate_index_to_half_of_list(self, index):
  return rotate_to_half(index, len(self.headarr))

 def distance_advancement_list(self, distance):
  start = self.get_target().x
  retn = []
  for i,head in enumerate(self.headarr):
   retn.append(start + (distance * self.rotate_index_to_half_of_list(i)))
  return retn

 def move_to_positions(self, distlist):
  for dt, hd in zip(distlist, self.headarr):
   hd.mv_x(dt)

 def advance_all_heads_by_distance(self, distance):
  self.move_to_positions(self.distance_advancement_list(distance))

 def pattern_advancement_list(self, pattern):
  # from the half of list, get the self.headarr[n] 
  start = self.get_target().x
  retn = [start]
  for head in self.headarr:
   try:
    beg, end = head.find_from(pattern, start)
   except AttributeError:
    end = 0
   start = end
   retn.append(beg)
  return retn

 def advance_all_heads_by_pattern(self, pattern):
  self.move_to_positions(self.pattern_advancement_list(pattern))

 def get_headnum(self):
  return len(self.headarr)

 def get_target(self):
  return self.headarr[self.target_head]

 def set_target(self, target_index):
  self.target_head = target_index % self.get_headnum()

 def set_target_next(self):
  self.set_target(self.target_head + 1)

 def set_target_previous(self):
  self.set_target(self.target_head - 1)

 def set_target_middle(self):
  self.set_target(self.rotate_index_to_half_of_list(-1))

 def set_target_last(self):
  self.set_target(-1)

 def render_all(self, size):
  def is_target(i):
   return i == self.target_head
  retn = []
  for i in range(self.get_headnum()):
   line = self.headarr[i].render(size, is_target(i))
   retn.append(self.relren(i, len(self.headarr), line))
  return retn

class VirtualTerminal():
 
 def __init__(self):
  self.pattern = ''

 def print_at_bottom(self, toprint):
  with terminal.location(0, terminal.height - 1):
   echo(toprint)

 def ex_mode(self, buffr='', prompt=':'):
  #capture instructions at the bottom
  with terminal.location(0, terminal.height - 1), terminal.raw():
   echo(prompt)
   while True:
    k = terminal.inkey()
    if k.name == 'KEY_ENTER': #heisenbug: you press enter, but don't exit ex mode
     echo('\r' + u' '*terminal.width)
     break
    elif k.name == 'KEY_BACKSPACE':
     if buffr:
      buffr = buffr[:-1]
      echo("" + u' ' + "")
     continue
    buffr += k
    echo(k)
   return buffr

 def show_to_terminal(self, heads):

  #Tag optimization: acumulate all changes to terminal to take advantage of the print buffer
  cumulative = ""
  rendrs = [renderers.render_fore_color, renderers.render_back_color, renderers.render_bold, renderers.render_italic, renderers.render_reverse]
  for i, fat in enumerate(heads.render_all(terminal.width)):
   print("\n\n\n", fat)
   terminal.inkey()
   try:
    cumulative += terminal.move_xy(0,i) + fat.compa(rendrs)
   except TypeError:
    print("\n\n\n\n\n\033[38;2;255;0;0m", fat)
    while True:
     terminal.inkey()
  print(cumulative, end='')
  echo('')

 def process_command(self, command, heads):

  if command == 'q':
   return False

  elif command == 'l':
   heads.get_target().mv_right()
  elif command == 'h':
   heads.get_target().mv_left()

  elif command == 'k':
   heads.set_target_previous()
  elif command == 'j':
   heads.set_target_next()
  elif command == ';':
   heads.set_target_middle()
  elif command == 'd':
   heads.set_target_last()

  # I like this: going '< on the first like takes you to the last line. It loops.
  # move the target line to the home position, advancing all the heads in the process
  elif command == '<':
   heads.advance_all_heads_by_distance(terminal.width)

  elif command == ':':
   command = self.ex_mode()
   self.print_at_bottom(eval(command))
  elif command == '/':
   self.pattern = self.ex_mode(prompt='/')
   heads.advance_all_heads_by_pattern(self.pattern)

  elif command == '>':
   heads.advance_all_heads_by_pattern(self.pattern)

  return True

 def interactive_loop(self, heads):

  def next_command():
   #Tag optimization: smaller time resolution for smaller sleep
   with timer_resolution(1):
    return terminal.inkey()

  with terminal.fullscreen(), terminal.hidden_cursor(), terminal.cbreak():
   cmd = ''
   while self.process_command(cmd, heads):
    self.show_to_terminal(heads)
    cmd = next_command()

 def main(self, infile, renderer=None):

  heads = HeadArray(down_to_closest_odd(terminal.height - 1), LoopRibbon(infile, renderer), select_background)
  heads.advance_all_heads_by_distance(terminal.width)
  heads.set_target_middle()

  self.interactive_loop(heads)

def background(graynum, fat):
 backd = "{0}{0}{0}".format(graynum)
 return pupil.StyleObj(["bbbbbb", backd, "0", "0", "0"], [fat])

def select_background(index, number, fat):
 rele = abs(rotate_to_half(index, number))
 retn = ''
 mo = rele % 4
 ma = rele % 8
 me = rele % 32

 if rele == 0:
  retn = background('6e', fat)

 elif me == 0 or me == 31:
  retn = background('64', fat)

 elif ma == 0 or ma == 7:
  retn = background('50', fat)

 elif mo == 1 or mo == 2:
  retn = background('00', fat)
 else:
  retn = background('1e', fat)
 return retn

def condense(chars):
 acum = ""
 retn = pupil.StyleObj([], [])
 for i in chars:
  if i == '\n':
   retn.slurp(acum)
   retn.slurp(pupil.StyleObj(['00ffff'], [i]))
   acum = ""
  elif i == '\t':
   retn.slurp(acum)
   retn.slurp(pupil.StyleObj(['00ffff'], [i]))
   acum = ""
  else:
   acum += i
 return retn

main = functools.partial(VirtualTerminal().main, renderer=condense)
