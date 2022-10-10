
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

#Pg informal testing

from encheiridion import enchi 

def mkup(char):
 retn = char
 if char == '\n':
  retn = pupil.StyleObj(['00ffff'], ['n'])
 elif char == '\t':
  retn = pupil.StyleObj(['00ffff'], ['t'])
 return retn

def todito(string):
 #make a styleobj with the simple cyan style from the given string
 data = []
 cumm = ""
 for i in string:
  curr = mkup(i)
  if type(curr) == str:
   cumm += i
  else:
   if cumm:
    data.append(cumm)
    cumm = ""
   data.append(curr)
 else:
  if cumm:
   data.append(cumm)
 retn = pupil.StyleObj(['cccccc'], data, [renderers.render_fore_color])
 return retn


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

 def slice(self, start, delta):
  return [self.source[i % len(self)] for i in range(start, start+delta)]

 def find_from(self, pattern, start):
  patn = re.compile(pattern)
  matched = patn.search(self.string, start)
  return matched.start(), matched.end()

 def render(self, start, delta):
  if self.renderer is not None:
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
  lista[pos] = terminal.reverse(lista[pos])
  return lista

 def render(self, width, target_flag=False):
  datt = self.track.render(self.x, width)
  if target_flag:
   texto = self.insert_cursor_at(datt, 0)
  else:
   texto = datt
  return "".join(texto)
