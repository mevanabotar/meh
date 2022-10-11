
import re
import iris.renderers as renderers

#Pg escape hack

def escapehack(rawstr):
 rawstr = re.sub(r"\[", r"<{<", rawstr)
 rawstr = re.sub(r"\]", r">}>", rawstr)
 return rawstr

def unescapehack(rawstr):
 rawstr = re.sub( r"<{<", r"[", rawstr)
 rawstr = re.sub( r">}>", r"]", rawstr)
 return rawstr


#Pg lexer

def behead(stylestr):
 """Separate the style overrides from the text."""
 head, body = stylestr[1:-1].split(" ", 1)
 return head, body

def caliper(body):
 """Return the boundaries of the next member section.

 It should detect 2 types of members: branches "[() this caliper [() no cause for fear [() not it, it doesn't hurt]]]"
                                    and leaves " it only helps me measure how much skin you have"
 You should be able to escape brackets:
                                               "[() on the topmost layer of fat \[I feel that this is backwards: the fat underneath the topmost layer of skin... but that might be harder to rhyme\]. But I won't make that incision, till you are nice and numb]"
 """
 nest = 0
 start = body.find('[') 
 for i, c in enumerate(body[start:]):
  if c == '[':
   nest += 1
  elif c == ']':
   nest -= 1

  if nest == 0:
   return start, i + 1

def is_styled_nest(member):
 return member[0] == '[' and member[-1] == ']'

def body_measurements(body):
 last = 0
 ranges = [last]
 a_little_of_you = caliper(body[last:])
 while a_little_of_you != (-1, -1):

  if a_little_of_you is None:
   break
  if a_little_of_you == (-1, 1):
   ranges.append(len(body) + 1)
   return ranges

  start, step = a_little_of_you
  last += start
  ranges.append(last)
  last += step
  ranges.append(last)

  a_little_of_you = caliper(body[last:])

 return ranges

def dismember(body):
 thespacebetween = body_measurements(body) #blue kid - the dismemberment song
 cutmarks = zip(thespacebetween, thespacebetween[1:])
 so_refreshing = [body[molar:jaw] for molar,jaw in cutmarks]
 return [i for i in so_refreshing if i] # for me ;)

def excerebrate(head):
 return head[1:-1].split(",")

def cut_you_up(stylestr):
 head, body = behead(stylestr)
 brain = excerebrate(head)
 members = dismember(body)
 return brain, members

#Pg compile

def wash_brains(brain):
 retn = []
 for i in brain:
  if not i:
   retn.append(None)
  else:
   retn.append(i)
 return retn

"""
[(parent,style) [(child,style) chile] atom style]
"""
class StackUnderflow(BaseException):
 pass

class StackRenderer():

 def __init__(self, styletree):
  """
  the styletree must be in string form, not yet lexed. So you start by lexing the current element in the element list, which is just one element long: the starting style tree.
  """

  self.styletree = styletree

 def top(self, stack):
  try:
   retn = stack[-1]
  except IndexError:
   raise StackUnderflow
  return retn 

 def down(self, stack):
  try:
   retn = stack[-2]
  except IndexError:
   raise StackUnderflow
  return retn 

 def save_styles(self, stackarray, brains):
  """Initialize the stackarray with the style elements

  incoming: ('ffffff','000000','1','1')
  outgoing: (True,True,True,True)
  side effect: [['ffffff', None], ['000000', None], ['1', None], ['1', None]]

  incoming: ('ff0000', None, '0')
  outgoing: (True,False,True)
  side effect: [['ffffff', None, 'ff0000', None], ['000000', None], ['1', None, '0', None], ['1', None]]

  incoming: ('ff0000', None, '1')
  outgoing: (False,False,True)
  side effect: [['ffffff', None, 'ff0000', None], ['000000', None], ['1', None, '0', None, '1', None], ['1', None]]

  incoming: overwrite_styles
  outgoing: updated style use stack array

  The None in each stack array is a use flag: if the top of the stack is None, the underlying style has not been applied in this sequence. Then it is rendered. If there is a stack value on top of the stack, that value is in effect right now.
  """
  undoes = []

  for stystack, stye in zip(stackarray, brains):

   #if the style is not overwritten, do nothing
   if stye is None:
    undoes.append(False)
    continue

   #if the new style is the same as the current style, do nothing
   #try:
    #if self.top(stystack) == stye:
     #undoes.append(False)
     #continue
    #elif self.down(stystack) == stye:
     #undoes.append(False)
     #continue
   #except StackUnderflow:
    #pass #if the stack is empty, there is something that needs application

   #if the style has been applied, unapply it
   try:
    if self.top(stystack) is not None:
     stystack.append(None)
   except StackUnderflow:
    # if the stack is empty, there is nothing to unapply
    pass

   #if this branch is overwriting the basal style, add and unapply current style
   if stye is not None:
    stystack.append(stye)
    stystack.append(None)
    undoes.append(True)

  return undoes #[True if i is not None else False for i in brains] #True for stacks that were modified

 def apply_styles(self, target, stylestacks, renderfuncs, tarmod=lambda x: x):
  """Render the target string applying the styles saved in stylestacks according to renderfuncs.

  The target is just a normal string.
  stylestacks is an interesting datastructure: A list of stacks. Each stack represents a style, and it matches the rendering function in renderfuncs with the same index. When a new style in the styletree is encountered, its pushed into the stylestack, then a None value that means "the underlying style has yet to be applied". This is how I save on reapplying styles whenever we go up a nesting level when it is still in effect.
  The renderfuncs take in the style as specified in a stylestack and convert it into a format acceptable by the target renderer. It creates the ansi codes. It might be more powerful if it could modify the target function too, but then you would need some logic to combine the returning targets without repetition?
  I'll just add an optional function to modify the target.
  """

  stye = ""
  for ste, fn in zip(stylestacks, renderfuncs):
   sye = ste.pop()
   if sye is None:
    sye = ste.pop()
    stye += fn(sye)
   ste.append(sye)
  return stye + tarmod(target)

 def clean_styles_stack(self, stylestacks, undoes, nxt=''):
  for sk, ud in zip(stylestacks, undoes):
   if ud:
    sk.pop()

 def compile_step(self, styleStacks, styletree):
  styles, members = cut_you_up(styletree)
  undoes = self.save_styles(styleStacks, wash_brains(styles))
  return undoes, members

 def compa(self, render_functions):
  stylestr = self.styletree
  brains, members = cut_you_up(stylestr)
  pending = []
  styleStacks = [[] for i in brains]
  undoStylesStack = []
  undo, body = self.compile_step(styleStacks, stylestr)
  elts = body
  retn = ""

  while True:
   
   if elts:
    if not is_styled_nest(elts[0]):
     retn += self.apply_styles(elts[0], styleStacks, render_functions)
     del elts[0]
    else:
     pending.append(elts[1:])
     undo, body = self.compile_step(styleStacks, elts[0])
     elts = body
     undoStylesStack.append(undo)

   elif pending:
    elts = pending.pop()
    self.clean_styles_stack(styleStacks, undoStylesStack.pop())
   else:
    return retn

 def __repr__(self):
  return str(self.styletree)

class StyleObj(StackRenderer):

 def __init__(self, styles, datalist, rendfuncs=[]):
  self.styles = styles
  self.data = datalist
  self.rendfuncs = rendfuncs

 def is_styleobj(self, obj):
  return type(obj) == type(self)

 def clean_styles_stack(self, stylestacks, undoes, nxt=''):
  if self.is_styleobj(nxt):
   stys = nxt.styles
  else:
   stys = [False] * len(undoes)

  for sk, ud, sts in zip(stylestacks, undoes, stys):
   print(self.top(sk), ud, sts)
   #if self.top(sk) == sts:
    #ud = False
   if ud:
    sk.pop()

 def compile_step(self, styleStacks, styles):
  undoes = self.save_styles(styleStacks, wash_brains(styles))
  return undoes

 def compa(self):
  # if called without arguments, return the unstyled string
  pending = []
  styleStacks = [[] for i in self.styles]
  undoStylesStack = []
  undo = self.compile_step(styleStacks, self.styles)
  elts = self.data
  retn = ""

  while True:

   #my own code is becoming a mystery to me
   if elts:
    if not self.is_styleobj(elts[0]):
     retn += self.apply_styles(elts[0], styleStacks, self.rendfuncs)
     elts = elts[1:]
    else:
     pending.append(elts[1:])
     undo = self.compile_step(styleStacks, elts[0].styles)
     elts = elts[0].data
     undoStylesStack.append(undo)

   elif pending:
    elts = pending.pop()
    print('\033[38;2;200;200;0m', elts, '\n', '\033[38;2;0;200;200m', pending, '\033[0m\n')
    nxt = ''
    if elts:
     nxt = elts[0]
    self.clean_styles_stack(styleStacks, undoStylesStack.pop(), nxt)
   else:
    return retn

 def indexed(self, index):
  pass

 def stylefields(self):
  def recur(elt):
   retn = len(elt.styles)
   for et in elt.data:
    if self.is_styleobj(et):
     retn = max(retn, recur(et))
   return retn
  return recur(self)

 def slurp(self, styleobj):
  self.data.append(styleobj)

 def bite(self, string):
  if type(self.data[-1]) is str:
   self.data[-1] += string
  else:
   self.slurp(string)

 def __len__(self):
  retn = sum([len(elt) for elt in self.data])
  return retn

 def __repr__(self):
  return str(self.styles) + str(self.data)

b = StyleObj(['bbbbbb', '550055', '1'], ["bruno franco", StyleObj(['','005500'], [" salamin"])], [renderers.render_fore_color, renderers.render_back_color, renderers.render_bold])
b.slurp(StyleObj(['bbbbbb'], ["brantley"]))
b.slurp(StyleObj(['bbbbbb'], [" perez"]))
b.slurp(StyleObj(['00bbbb'], [" saavedra"]))
b.bite(" calvo")
b.slurp(StyleObj(['aa00aa'], ['uno']))
b.slurp(StyleObj(['aa00aa'], ['dos']))
b.bite("tres")
b.slurp(StyleObj(['aa00aa'], ['cuatro']))
b.bite("cinco")
b.slurp(StyleObj(['aa00aa'], ['seis']))
