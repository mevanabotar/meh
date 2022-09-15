
"""
styles: (hexforegroundcolor,hexbackgroundcolor,5bitInt,fontName)
rendered format: [(local) " string" [(local) [() "another string"] "yet another string  " "and another"] "one more"]
ideas: downstream overriding?
"""

class Marked():
 def __init__(self, styles, overrides, *values):
  self.vals = values
  self.styles = zip(overrides, styles)

 def __repr__(self):
  return str(list(self.styles)) + " " + str(self.vals)

def style(fore=0xffffff, back=0x000000, bold=0, blink=0):
 return (fore, back, bold, blink)

def trans(local, override=tuple(), *values):
 #implemented: foreground
 return [(local, override)] + list(values)
 
a = "[(ff0000) blanco [(ffffff) red] [() white] [(0000ff) blue [(00ffff) cyan nested]] [() normal]]"

"""
a pushdown automaton could implement the nesting logic...
the current style is the top of the stack
to make the current style, copy the previous style and override the specified parameters
leaving the nested format pops the stack
a [ pushes the new style on the stack
a ] pops the current style on the stack
an emtpy style copies the previous style

 BOTTOM
ffffff 000000
ff0000 000000
ff0000 222222
 TOP

"""
 


