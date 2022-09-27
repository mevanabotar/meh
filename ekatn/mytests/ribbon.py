
#Pg Documentation
"""
here are my ideas
the mvp is a list of characters and a cursor. A cursor has a position in the character list, and when queried returns the character at that position.
"""

#Pg TODO

# TODO1
#1 get the character list
#2 turn them to binary
#3 make a cursor
#4 position the cursor
#4.1 move the cursor
#5 query the cursor for position

# TODO2 have the cursor store information from the tape, and pass that information to a third program for processing. That third program can be a function in python or an external command called from a pipe. The output of the program should be captured and returned.
#1 store everything from current position to given index. If the index is negative, store it in reverse xD
#2 store everything between two given indexes a,b
#2.1 if b<a, store it in reverse
#3 pass the stored thing to a given function
#4 pass the stored thing to a given external program
#5 return the output of the program

# TODO3 interfacing with a window
# make a widget where the cursor can print some data from the ribbon
#1 load a running widget with data
#2 make a one line widget within the current window
#2.1 push trash into the running widget
#3 make the widget ask its associated cursor for data on some event
#4 have a cursor on the widget
#5 change name of cursor class to Head, have the cursor just be the visual thing in the widget
#6 move the cursor within the widget, left and right


#Pg prototype

#TD 1,2
with open('encheiridion.txt') as t:
 bk = t.read()
bka = bk.encode('utf-8')

#TD 3
class Head():
 def __init__(self, track, x=0):
  self.x = x # the cursor's position on the tape
  self.data = "" # the outpipe data
  self.track = track

 #Pg reading
 def peek(self, ribbonfile):
  return ribbonfile[self.x]

 #TD2 1
 def read_till(self, end):
  self.data = self.track[self.x: end]

 #TD2 2
 def read_index(self, start, end):
  self.data = self.track[start:end]

 #TD2 3
 def process_with(self, fn):
  return fn(self.data)


 #Pg movement
 #TD 4
 def mvabs(self, x):
  self.x = x

 def mvrel(self, d):
  self.x += d

 def step_forward(self):
  self.mvrel(1)

 def step_backward(self):
  self.mvrel(-1)

h = Head(bk)

#Pg Glossary
"""
ribbon = a binary list/thing in memory that gets read and interacted with by a cursor. You can think of it as the internal representation of the file.
"""

#Pg Planning
"""
Should cursors be directly associated with a ribbon?
Should I always pass the ribbon to use for a cursor?

Should ribbons be their own class?
 There are properties that are better associated with the ribbon than the cursor:
  the length of the ribbon
  the number of characters
  the encoding
  the source file
  the modifying functions, like
   saving to file,
   the undo/redo history/tree
  preferred markup?
 Just for the undo/redo capability, it should be its own class. I'll do that later, when the complexity is warranted.

I want the special show cursor to have two ribbons with it:
 the text ribbon
 the render ribbon
the text ribbon is the text to read
the render ribbon is the markup of that text
Would that cursor then have the program to combine the text and the render?
If I prerender the markup of the text, will that make the program faster? Am I getting something by sacrificing space like that?

Could I have virtual ribbons?
 ribbons that don't have underlying text, but return some text when queried and behave exactly like ribbons?
 Can render ribbons be virtual ribbons?
  that take as input the text to be rendered?
   

"""

