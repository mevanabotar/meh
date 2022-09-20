
import unittest

#Pg lexer

def behead(stylestr):
 head, body = stylestr[1:-1].split(" ", 1)
 return head, body

def member_measure(body):
 nest = 0
 start = body.find('[') 
 for i, c in enumerate(body[start:]):
  if c == '[':
   nest += 1
  elif c == ']':
   nest -= 1

  if nest == 0:
   return start, i + 1

def calipers(body):
 last = 0
 ranges = [last]
 a_little_of_you = member_measure(body[last:])
 while a_little_of_you != (-1, -1):

  if a_little_of_you is None:
   break

  start, step = a_little_of_you
  last += start
  ranges.append(last)
  last += step
  ranges.append(last)

  a_little_of_you = member_measure(body[last:])

 return ranges

def dismember(body):
 thespacebetween = calipers(body) #blue kid - the dismemberment song
 cutmarks = zip(thespacebetween, thespacebetween[1:])
 so_refreshing = [body[molar:jaw] for molar,jaw in cutmarks]
 return so_refreshing # for me ;)

def excerebrate(head):
 return head[1:-1].split(",")

def butcher(stylestr):
 head, body = behead(stylestr)
 brain = excerebrate(head)
 members = dismember(body)
 return brain, members

class TestLexer(unittest.TestCase):
 def test_dismemberment(self):
  self.assertEqual(
    butcher('[(ffffff,310000) this will be [(200,30,30) ooh!] this will be [(200,30,30) aah!] this will be [(200,30,30) absolutely [(200,0,200) whee!]]]'),
    (['ffffff', '310000'], ['this will be ', '[(200,30,30) ooh!]', ' this will be ', '[(200,30,30) aah!]', ' this will be ', '[(200,30,30) absolutely [(200,0,200) whee!]]']))

#Pg compile

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

"""

class StackRenderer():
 def __init__(self, stylestr):

 def make_nested_format(self, brains):
  previous = self.stack[-1]
  return previous

 def compile(self, stylestr):
  brains, members = butcher(stylestr)
  self.stack.append(self._make_nested_format(brains))
  print(self.stack)


class TestCompile(unittest.TestCase):
 def test_discriminate_nested(self):
  brains, members = butcher('[(ffffff,310000) this will be [(200,30,30) ooh!] this will be [(200,30,30) aah!] this will be [(200,30,30) absolutely [(200,0,200) whee!]]]')
  self.assertEqual([is_styled_nest(i) for i in members], [False, True, False, True, False, True])

if __name__ == "__main__":
 unittest.main()
