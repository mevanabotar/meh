
import blessed
from random import randint
import re


"Get the test file"
testfile = 'encheiridion.txt'
with open(testfile, encoding='utf8') as tf:
 tst = tf.read()

terminal = blessed.Terminal()

def echo(toprint):
 """Print to terminal, always flushing and end in ''."""
 print(toprint, end='', flush=True)

#Pg helpers

def keywity(context_man):
 """Read a key pressed in the given context. Used for debugging."""
 with context_man():
  return terminal.inkey()

#Pg cursor
"""TODO

DONE
1) have a cursor in a line with text
2) move the cursor ahead and behind
3) get the character under the cursor
4) print the character under the cursor
5) print line from cursor position


6) jump to pattern match
7) jump back and forth on pattern matches
a) multiple pattern search
b) highlight different pattern searches with different markups
c) ex command goto
d) the ex command buffer should itself be a Head()
e) highlight the window on which the ex mode is operating

8) print many lines of the text, each a window into a newline of the text
9) select a window to move in
10) align all windows on `pattern`

11) modify the text buffer
12) undo the modification
13) save modifications to a file
14) update all windows when you modify the text
15) update certain windows when you modify the text
16) update selected windows
17) select windows by number
18) print window number
19) group selected windows

20) markup text
21) make your own markup for the current window
22) select a premade markup for the current window
23) search by markup
"""

#Pg T0.1

class Memo():
 def __init__(self):
  self.tst = "En la hora de angustia y de luz vaga, en su Golem los ojos detenia. Quien nos diria lo que sentia Dios, al mirar a su rabino en Praga?"
  self.rangehash = {}

 def add_slice(self, start, delta, vals):
  self.rangehash[(start,delta)] = vals

 def add_tst(self, start, delta, source):
  self.add_slice(start, delta, source[start:start+delta])

 def get_slice(self, start, delta):
  for ky in self.rangehash:
   st, da = ky
   if st <= start and (start + delta) <= da:
    return self.rangehash[ky][start:start+delta]
  return None

 def fuse(self, cumulative, current):
  #[(start, delta), value]
  cumu_start, cumu_delta = cumulative[0]
  cumu_val = cumulative[1]
  curr_start, curr_delta = current[0]
  curr_val = current[1]

  new_start = cumu_start
  difference = curr_start - cumu_start
  new_delta = difference + curr_delta
  return (new_start, new_delta) , cumu_val[0: difference] + curr_val

 def is_within(self, cumulative, current):
  cumu_start, cumu_delta = cumulative[0]
  cumu_end = cumu_start + cumu_delta
  curr_start, curr_delta = current[0]
  curr_end = curr_start + curr_delta

  return cumu_start <= curr_start and curr_end <= cumu_end

 def is_overlap(self, cumulative, current):
  cumu_start, cumu_delta = cumulative[0]
  cumu_end = cumu_start + cumu_delta
  curr_start, curr_delta = current[0]
  curr_end = curr_start + curr_delta

  return cumu_start <= curr_start and curr_start <= cumu_end

 def consolidate(self):

  if len(self.rangehash) < 1:
   return self.rangehash
  cumulative, *ordenado = sorted(list(self.rangehash.items()))
  retn = {}

  def save(sliced):
   key, val = sliced
   retn[key] = val

  def following():
   try:
    retn = ordenado[0]
    del ordenado[0]
   except IndexError:
    retn = []
   return retn

  while True:
   
   current = following()
   if current:
    if self.is_within(cumulative, current):
     pass
    elif self.is_overlap(cumulative, current):
     cumulative = self.fuse(cumulative, current)
    else:
     save(cumulative)
     cumulative = current
   else:
    save(cumulative)
    break
  self.rangehash = retn

 def __repr__(self):
  return str(self.rangehash)

atst = Memo()
atst.add_tst(0,5,atst.tst)
atst.add_tst(4, 10, atst.tst)
atst.add_tst(9,20, atst.tst)
atst.add_tst(30,10,atst.tst)
atst.add_tst(50,2,atst.tst)
atst.add_tst(30,5, atst.tst)
atst.add_tst(10,5, atst.tst)


#Tag optimization: reduce the number of calls to render by memoizing already rendered values
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

 def mapping(self, chars):
  retn = []
  for i in chars:
   if i == '\n':
    retn.append(terminal.cyan + 'n' + terminal.normal)
   elif i == '\t':
    retn.append(terminal.cyan + 't' + terminal.normal)
   else:
    retn.append(i)
  return retn

 def render(self, start, delta):
  if self.renderer is not None:
   prerendered = self.rendered.get_slice(start, delta) 
   if prerendered is not None:
    return prerendered
   hererendered = self.renderer(self.slice(start, delta))
   self.rendered.add_slice(start, delta, hererendered)
   self.rendered.consolidate()
   return hererendered 
  return self.mapping(self.slice(start, delta))

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

 def mv_find_from(self, pattern, start):
  s, e = self.track.find_from(pattern, start)
  self.mv_x(s)
  return s, e

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
"""
1) have 2 cursors, each running on a different line, with different views of the file
2) move between the two cursors to interact with them with jk
3) make terminal.height-1 cursors, printed from top to bottom
4) move to the bottom cursor
5) move to the top cursor
6) select cursors to coordinate
7) advance all cursors by pattern (\n)
   send to grouped cursors the same message

8) highlights: color the lines based on their relative position

-2
-1
0
1
2
"""

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

def ex_mode(buffr='', prompt=':'):
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

from blessedtst import ekatn, rendr, prerendr

def renderizador(lista):
 retn = []
 for i in lista:
  retn.append(rendr(ekatn(i)))
 return retn 

def down_to_closest_odd(num):
 offset = (num - 1) % 2
 return num - offset

def main(infile, renderer=None):

 from kairos import timer_resolution

 heads = HeadArray(down_to_closest_odd(terminal.height - 1), infile, renderer)
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
    command = ex_mode()
    ex_mode(prompt=eval(command))
   elif ky == '/':
    pattern = ex_mode(prompt='/')
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
