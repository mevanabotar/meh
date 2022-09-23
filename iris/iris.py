
import unittest
import renderers

#Pg lexer

def behead(stylestr):
 """Separate the style overrides from the text."""
 head, body = stylestr[1:-1].split(" ", 1)
 return head, body

def caliper(body):
 """Return the boundaries of the next member section.

 It should detect 2 types of members: branches "[() this caliper [() no cause for fear [() not it, it doesn't hurt]]]"
                                    and leaves " it only helps me measure how much skin you have"
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

class TestLexer(unittest.TestCase):
 def test_dismemberment(self):
  self.assertEqual(
    cut_you_up('[(ffffff,310000) this will be [(200,30,30) ooh!] this will be [(200,30,30) aah!] this will be [(200,30,30) absolutely [(200,0,200) whee!]] this will be nice]'),
    (['ffffff', '310000'], ['this will be ', '[(200,30,30) ooh!]', ' this will be ', '[(200,30,30) aah!]', ' this will be ', '[(200,30,30) absolutely [(200,0,200) whee!]]', ' this will be nice']))

#Pg compile

def wash_brains(brain):
 retn = []
 for i in brain:
  if not i:
   retn.append(None)
  else:
   retn.append(i)
 return retn

def is_styled_nest(member):
 return member[0] == '[' and member[-1] == ']'

def inherit(lsta, lstb):
 #lstb inherits from lsta. values in lstb overrite values in lsta.
 #[1,0,0,1,2,1] [None,None,3,None,4] -> [1,0,3,1,4,1]
 retn = []
 for i in range(len(lsta)):
  try:
   if lstb[i] is None:
    retn.append(lsta[i])
   else:
    retn.append(lstb[i])
  except IndexError:
   return retn + lsta[i:]
 return retn

"""
[(parent,style) [(child,style) chile] atom style]

TODO:

get the first style, the root style, from the style string. the remaining style string should still be valid. like
 [(ffffff,000000) white over black [(,310000) white over dark red]] ->
 (ffffff,000000) [() white over black [(,310000) white over dark red]] or
 (ffffff,000000) [(ffffff,000000) white over black [(,310000) white over dark red]]
the point is this: I don't need a special case for when the stack is empty, since the stack never starts empty.

create the next styledish by inheriting from the previous styledish
 stack: (ffffff,000000,1,0) (,,10,1) &
 stack: (ffffff,000000,1,0) (ffffff,ffffff,10,1)

render the stylestring into ansi escape codes
 [(ff0000,222222,1) bold red over dark gray] ->
 \033[38;2;255;0;0m\033[48;2;22;22;22mbold red over dark gray

render current style on entering nesting
 (ffffff,000000,1) [(,,0,1) non bold italicized]
 (ffffff,000000,1) (ffffff,000000,0,1)
                   non bold italicized

restore previous style on exit nesting
 (ffffff,000000,1) [(,,0,1) non bold italicized] white bold
 (ffffff,000000,1) (ffffff,000000,0,1)
                   non bold italicized
 white bold
white                 black           white                 black           bold   reset  white                 black           italic                    reset  white                 black           bold
\033[38;2;255;255;255m\033[48;2;0;0;0m\033[38;2;255;255;255m\033[48;2;0;0;0m\033[1m\033[0m\033[38;2;255;255;255m\033[48;2;0;0;0m\033[3mnon bold italicized\033[0m\033[38;2;255;255;255m\033[48;2;0;0;0m\033[1m

dog, these format strings are effing long! make an optimizing renderer...
 selective reset of characteristics: instead of blasting all style with \033[0m, undo specific styles as required
  unbolden, unitalic, ununderlined. instead of uneverything and redo
  (white,black,bold) (,,0,italic) ->
  white black bold unbold italic
 smush inherited styles
  (white,black,bold) (,,,underlined) ->
  white black bold underlined

  white black bold white black bold underlined



Glossary:
 styledish: each level in the style stack
 stylestring: the nested representation of a markup string, [(val,val) string string [(val) string] [(,val) string]]
 basal: closer to the root
 apical: closer to the leafs

"""

"""
if current_stylenest is empty:
 clean your stack changes
 

if  the current element  is  a stylenest:
 save its styling info into the stylestacks
 save the rest of the current stylenest to the styletree stack
 current_stylenest = dismember(current element)
else:
 render it with the current style
"""

tstsave = """[(ffffff,000000,1) this is no orthodox [(,555555) beheading] [(,,0) I'm cuting you [(ff0000) up] cutting you up] cutting you up will be so refreshing to me]"""

tstcompilation = [
        '[(ff0000,440000,1) bold red on dark red]',
        '[(00ff00,440000,1) Im green over dark red and bold! [(0000ff) but I feel all blue]]',
        '[(ff00ff,000000) [(,bbbb00) magenta over yellow] [(,00bbbb) magenta over cyan] [(,0000bb) magenta over blue] just magenta]',
        '[(ffffff,007700,0,0) white over green darkish [(,,1) Im just bold [(,,,1) Im bold and italic!] just bold again] Ive been restored to my previous glory]'
        ]
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

 def save_styles(self, stackarray, brains):
  """Initialize the stackarray with the style elements

  incoming: ('ffffff','000000','1','1')
  outgoing: (True,True,True,True)
  side effect: [['ffffff', None], ['000000', None], ['1', None], ['1', None]]

  incoming: ('ff0000', None, '0')
  outgoing: (True,False,True)
  side effect: [['ffffff', None, 'ff0000', None], ['000000', None], ['1', None, '0', None], ['1', None]]

  incoming: overwrite_styles
  outgoing: updated style use stack array

  The None in each stack array is a use flag: if the top of the stack is None, the underlying style has not been applied in this sequence. Then it is rendered. If there is a stack value on top of the stack, that value is in effect right now.
  """
  for stystack, stye in zip(stackarray, brains):

   #if the style is not overwritten, do nothing
   if stye is None:
    continue

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

  return [True if i is not None else False for i in brains] #True for stacks that were modified

 def apply_styles(self, target, stylestacks, renderfuncs):
  stye = ""
  for ste, fn in zip(stylestacks, renderfuncs):
   sye = ste.pop()
   if sye is None:
    sye = ste.pop()
    stye += fn(sye)
   ste.append(sye)
  return stye + target

 def clean_styles_stack(self, stylestacks, undoes):
  for sk, ud in zip(stylestacks, undoes):
   if ud:
    sk.pop()

 def compile_step(self, styleStacks, styletree):
  styles, members = cut_you_up(styletree)
  undoes = self.save_styles(styleStacks, wash_brains(styles))
  return undoes, members

 def compa(self, stylestr, render_functions):
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


class TestCompile(unittest.TestCase):
 def test_discriminate_nested(self):
  brains, members = cut_you_up('[(ffffff,310000) this will be [(200,30,30) ooh!] this will be [(200,30,30) aah!] this will be [(200,30,30) absolutely [(200,0,200) whee!]]]')
  self.assertEqual([is_styled_nest(i) for i in members], [False, True, False, True, False, True])

if __name__ == "__main__":
 unittest.main()
