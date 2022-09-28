
#Pg imports
from random import randint
import re
import functools

import blessed

from mytests.blessedtst import ekatn, rendr, prerendr, simplemap1, incompletemap1
from mytests.kairos import timer_resolution
from memoization import Memo


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
   #Tag optimization: reduce the number of calls to render by memoizing already rendered values
   prerendered = self.rendered.get_slice(start, delta) 
   if prerendered is not None:
    return prerendered

   hererendered = self.renderer(self.slice(start, delta))
   self.rendered.add_slice(start, delta, hererendered)
   self.rendered.consolidate()
   return hererendered 

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
  lista[pos] = terminal.reverse(lista[pos])
  return lista

 def render(self, width, target_flag=False):
  datt = self.track.render(self.x, width)
  if target_flag:
   texto = self.insert_cursor_at(datt, 0)
  else:
   texto = datt
  return "".join(texto)

# multilines

class HeadArray():

 def __init__(self, headnum, tape='', renderer=None):

  self.datass = LoopRibbon(tape, renderer)
  self.headarr = [Head(0, self.datass.duplicate()) for i in range(headnum)]
  self.target_head = 0

 def rotate_index_to_half_of_list(self, index):
  return index - len(self.headarr) //2

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

 def background(self, graynum, fat):
  backd = terminal.on_color_rgb(graynum, graynum, graynum)
  return backd + fat + terminal.normal

 def select_background(self, index, fat):
  rele = abs(self.rotate_index_to_half_of_list(index))
  retn = ''
  mo = rele % 4
  ma = rele % 8
  me = rele % 32

  if rele == 0:
   retn = self.background(110, fat)

  elif me == 0 or me == 31:
   retn = self.background(100, fat)

  elif ma == 0 or ma == 7:
   retn = self.background(80, fat)

  elif mo == 1 or mo == 2:
   retn = self.background(0, fat)
  else:
   retn = self.background(30, fat)
  return retn

 def render_all(self, size):
  def is_target(i):
   return i == self.target_head
  retn = []
  for i in range(self.get_headnum()):
   line = self.headarr[i].render(size, is_target(i))
   retn.append(self.select_background(i, line))
  return retn

def renderizador(lista):
 retn = []
 for i in lista:
  retn.append(rendr(ekatn(i)))
 return retn 

class VirtualTerminal():

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

 def down_to_closest_odd(self, num):
  offset = (num - 1) % 2
  return num - offset

 def main(self, infile, renderer=None):

  heads = HeadArray(self.down_to_closest_odd(terminal.height - 1), infile, renderer)
  heads.advance_all_heads_by_distance(terminal.width)

  with terminal.fullscreen(), terminal.hidden_cursor(), terminal.cbreak():
   heads.set_target_middle()
   ky = ''

   while True:

    if ky == 'q':
     break

    elif ky == 'l':
     heads.get_target().mv_right()
    elif ky == 'h':
     heads.get_target().mv_left()

    elif ky == 'k':
     heads.set_target_previous()
    elif ky == 'j':
     heads.set_target_next()
    elif ky == ';':
     heads.set_target_middle()
    elif ky == 'd':
     heads.set_target_last()

    # I like this: going '< on the first like takes you to the last line. It loops.
    # move the target line to the home position, advancing all the heads in the process
    elif ky == '<':
     heads.advance_all_heads_by_distance(terminal.width)

    elif ky == ':':
     command = self.ex_mode()
     self.ex_mode(prompt=eval(command))
    elif ky == '/':
     pattern = self.ex_mode(prompt='/')
     heads.advance_all_heads_by_pattern(pattern)

    elif ky == '>':
     heads.advance_all_heads_by_pattern(pattern)

    #Tag optimization: acumulate all changes to terminal to take advantage of the print buffer
    cumulative = ""
    for i, fat in enumerate(heads.render_all(terminal.width)):
     cumulative += terminal.move_xy(0,i) + fat
    print(cumulative, end='')
    echo('')

    #Tag optimization: smaller time resolution for smaller sleep
    with timer_resolution(1):
     ky = terminal.inkey()

main = functools.partial(VirtualTerminal().main, renderer=simplemap1)
#main = VirtualTerminal().main
