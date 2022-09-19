
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

class StackRenderer():
 def __init__(self, stylestr):
  self.stack = [['ffffff', '000000']]

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
