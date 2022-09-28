
import blessed as b

term = b.Terminal()

#Pg screen tests

def keytake():
 with term.cbreak():
  return term.inkey()

def fullscreentest():
 with term.fullscreen(), term.cbreak():
  print(term.move_y(term.height // 2) + term.center('press anything').rstrip())
  term.inkey()

def colortest():
 for r in range(0, 256, 16):
  for g in range(0, 256, 16):
   for b in range(0, 256, 16):
    print(term.color_rgb(r,g,b) + "a" + term.normal, end="")
   print(" ", end="")
  print()


def keytest():
 print(f"{term.home}{term.black_on_skyblue}{term.clear}")
 print("press 'q' to quit.")
 with term.cbreak():
     val = ''
     while val.lower() != 'q':
         val = term.inkey(timeout=3)
         if not val:
            print("It sure is quiet in here ...")
         elif val.is_sequence:
            print("got sequence: {0}.".format((str(val), val.name, val.code)))
         elif val:
            print("got {0}.".format(val))
     print(f'bye!{term.normal + term.clear}')

def bottom():
 print(f"{term.home + term.clear}")
 with term.cbreak():
  while True:
   k = term.inkey()
   if k == ':':
    with term.location(0, term.height - 1):
     print(":", end='', flush=True)
     while True:
      k = term.inkey()
      if k == '\n':
       break
      print(f"{k}", end='', flush=True)
   else:
    print(f"{k}", end='', flush=True)

#Pg color tests

def echo(arg):
 print(arg, end='', flush=True)

def gen_rgb(top, length):
 space = [top] + [0] * length
 idx = 0
 state = 0
 while True:
  
  yield space

  if state == 0:
   place = (idx+1) % len(space)
   space[place] += 1
   if space[place] == top:
    idx = place
    state = 1

  if state == 1:
   place = (idx-1) % len(space)
   space[place] -= 1
   if space[place] == 0:
    state = 0

def colorwheel(num):
 length = 2
 cspace = gen_rgb(num, length)
 for i in range((num*2+1)*(length+1)):
  vals = [i*(255//num) for i in next(cspace)]
  print(term.color_rgb(*vals) + "a" + term.normal, end="", flush=True)


def colores(palette):

 palette = [[i*16, j*16, k*16] for i,j,k in palette]
 for cs in palette:
  echo(term.color_rgb(*cs) + "0" + term.normal)

#Pg highlight maps

def high(numr):
 return numr >> 4
def low(numr):
 return numr - ((numr >> 4) << 4 )

hex_sex_asymmetric_chromatic_dark = [
   (16,0,0),
   (10,0,0),
   (16,8,0),
   (10,6,0),
   (16,16,0),
   (10,10,0),
   (10,16,0),
   (0,16,0),
 
   (0,10,0),
   (0,16,10),
   (0,16,16),
   (0,10,16),
   (0,0,16),
   (8,0,16),
   (16,0,16),
   (16,0,10)
   ]

hex_octo_symmetric_bright_dark = [
   (16,0,0),
   (16,8,0),
   (8,16,0),
   (0,16,8),
   (0,16,16),
   (0,8,16),
   (8,0,16),
   (16,0,8),

   (11,0,0),
   (11,7,0),
   (7,11,0),
   (0,11,7),
   (0,11,11),
   (0,7,11),
   (7,0,11),
   (11,0,7),
   ]

doz_symmetric_chromatic = [
   (16,0,0),
   (16,8,0),
   (16,16,0),
   (8,16,0),
   (0,16,0),
   (0,16,8),

   (0,16,16),
   (0,8,16),
   (0,0,16),
   (8,0,16),
   (16,0,16),
   (16,0,8),
   ]

hex_octo_asymmetric_light_dark = [
   (16,0,0),
   (16,8,0),
   (16,16,0),
   (0,16,0),

   (0,16,16),
   (0,8,16),
   (2,2,16),
   (16,0,16),


   (11,0,0),
   (11,7,0),
   (11,11,0),
   (0,11,0),

   (0,11,11),
   (0,7,11),
   (2,2,11),
   (11,0,11),
   ]

letter_short_high = "aeioumns" + "pbtdkgfh"
letter_short_high_vowel_mix = "avemonur" + "ifjpwbyl"

def ekatn(number):
 letter = letter_short_high_vowel_mix
 color = hex_octo_asymmetric_light_dark
 if number == 0:
  return ((9*16,9*16,9*16), '.')
 return (i*16 for i in color[high(number)]), letter[low(number)]
 
def rendr(number):
 return term.color_rgb(*number[0]) + number[1] + term.normal

def prerendr(number):
 return term.color_rgb(*number[0]) + number[1]

def testekatn():
 for i in range(256):
  echo(rendr(ekatn(i)))

def simplemap1(chars):
 retn = []
 for i in chars:
  if i == '\n':
   retn.append(term.cyan + 'n' + term.normal)
  elif i == '\t':
   retn.append(term.cyan + 't' + term.normal)
  else:
   retn.append(i)
 return retn

def incompletemap1(chars):
 retn = []
 for i in chars:
  if i == '\n':
   retn.append(term.cyan + 'n')
  elif i == '\t':
   retn.append(term.cyan + 't')
  else:
   retn.append(i)
 return retn

